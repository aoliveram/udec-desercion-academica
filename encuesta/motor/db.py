"""SQLite persistence layer.

Plain sqlite3 (no Streamlit imports) so the standalone scripts in scripts/ can
use it too. The Streamlit app wraps `connect()` in `st.cache_resource`.
"""

import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

from motor import settings

# Every session in the Streamlit process shares one sqlite3.Connection
# (check_same_thread=False, cached via st.cache_resource). Without this,
# two respondents' writes can interleave inside the same transaction --
# audit.append_event's "read the last row_hash, then insert" is the
# sharpest case: two concurrent appends can both read the same prev_hash
# and fork the chain, which verificar_integridad.py then reports as
# tampering that never happened. Write volume here is low (one row per
# widget interaction), so serializing costs nothing.
_write_lock = threading.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS respondents (
    id TEXT PRIMARY KEY,
    resume_token_hash TEXT UNIQUE NOT NULL,
    nomina TEXT NOT NULL,
    instrument_version TEXT,
    created_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('in_progress', 'completed', 'declined')),
    ip_hash TEXT,
    survey_data_json TEXT NOT NULL DEFAULT '{}',
    data_checksum TEXT
);

CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    respondent_id TEXT NOT NULL REFERENCES respondents(id),
    question_id TEXT NOT NULL,
    page_index INTEGER NOT NULL,
    value_json TEXT NOT NULL,
    first_answered_at TEXT NOT NULL,
    last_updated_at TEXT NOT NULL,
    time_spent_seconds REAL,
    UNIQUE (respondent_id, question_id)
);

CREATE TABLE IF NOT EXISTS page_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    respondent_id TEXT NOT NULL REFERENCES respondents(id),
    page_index INTEGER NOT NULL,
    entered_at TEXT NOT NULL,
    left_at TEXT,
    duration_seconds REAL
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    respondent_id TEXT,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    prev_hash TEXT NOT NULL,
    row_hash TEXT NOT NULL
);

-- One row per roster name that a respondent has picked in "¿Quién eres tú?".
-- The primary key is what makes "first one wins" hold: two respondents
-- picking the same name at the same moment can't both insert it.
CREATE TABLE IF NOT EXISTS name_claims (
    nomina TEXT NOT NULL,
    self_code TEXT NOT NULL,
    respondent_id TEXT NOT NULL REFERENCES respondents(id),
    claimed_at TEXT NOT NULL,
    PRIMARY KEY (nomina, self_code)
);

CREATE TABLE IF NOT EXISTS rate_limit (
    ip_hash TEXT PRIMARY KEY,
    window_start TEXT NOT NULL,
    count INTEGER NOT NULL
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect(db_path=None) -> sqlite3.Connection:
    db_path = db_path or settings.DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.executescript(SCHEMA)
    conn.commit()
    try:
        db_path.chmod(0o600)
    except (AttributeError, FileNotFoundError, OSError):
        pass
    return conn


@contextmanager
def transaction(conn: sqlite3.Connection):
    with _write_lock:
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise


# --- respondents ---------------------------------------------------------


def create_respondent(conn, respondent_id, token_hash, nomina, instrument_version, ip_hash):
    ts = now_iso()
    with transaction(conn):
        conn.execute(
            """
            INSERT INTO respondents
                (id, resume_token_hash, nomina, instrument_version, created_at, last_seen_at,
                 status, ip_hash, survey_data_json)
            VALUES (?, ?, ?, ?, ?, ?, 'in_progress', ?, '{}')
            """,
            (respondent_id, token_hash, nomina, instrument_version, ts, ts, ip_hash),
        )


def get_respondent_by_token_hash(conn, token_hash):
    return conn.execute(
        "SELECT * FROM respondents WHERE resume_token_hash = ?", (token_hash,)
    ).fetchone()


def get_respondents(conn, nomina):
    """Every respondent of a roster, whatever their status, oldest first."""
    return conn.execute(
        "SELECT * FROM respondents WHERE nomina = ? ORDER BY created_at",
        (nomina,),
    ).fetchall()


def touch_respondent(conn, respondent_id):
    with transaction(conn):
        conn.execute(
            "UPDATE respondents SET last_seen_at = ? WHERE id = ?",
            (now_iso(), respondent_id),
        )


def save_survey_blob(conn, respondent_id, data_json: str, checksum: str):
    with transaction(conn):
        conn.execute(
            """
            UPDATE respondents
            SET survey_data_json = ?, data_checksum = ?, last_seen_at = ?
            WHERE id = ? AND status = 'in_progress'
            """,
            (data_json, checksum, now_iso(), respondent_id),
        )


def mark_completed(conn, respondent_id):
    with transaction(conn):
        conn.execute(
            """
            UPDATE respondents
            SET status = 'completed', completed_at = ?
            WHERE id = ? AND status = 'in_progress'
            """,
            (now_iso(), respondent_id),
        )


def mark_declined(conn, respondent_id, consent_question_id, consent_value):
    """The respondent didn't consent (or withdrew consent after going back to
    that page). Everything they answered is deleted and their roster name is
    released; only the decision itself is kept, so declines can be counted.
    """
    blob = json.dumps({consent_question_id: {"value": consent_value}})
    with transaction(conn):
        conn.execute("DELETE FROM answers WHERE respondent_id = ?", (respondent_id,))
        conn.execute("DELETE FROM name_claims WHERE respondent_id = ?", (respondent_id,))
        conn.execute(
            """
            UPDATE respondents
            SET status = 'declined', completed_at = ?, survey_data_json = ?, data_checksum = NULL
            WHERE id = ? AND status = 'in_progress'
            """,
            (now_iso(), blob, respondent_id),
        )


# --- name claims (who is "¿Quién eres tú?" already taken by) ----------------


def claim_name(conn, nomina, self_code, respondent_id) -> str:
    """Try to claim a roster name for this respondent. Returns:

    - "claimed": it was free and now belongs to this respondent
    - "held":    this respondent already held it (re-render, resume)
    - "taken":   someone else got there first -- nothing changes

    A respondent holds at most one name: a successful claim releases any
    other name they'd claimed before (they changed their mind). A failed
    one leaves their existing claim alone. The insert is ON CONFLICT DO
    NOTHING against the primary key rather than check-then-insert, so
    it stays correct even if a second process is writing to the same file.
    """
    with transaction(conn):
        cur = conn.execute(
            """
            INSERT INTO name_claims (nomina, self_code, respondent_id, claimed_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (nomina, self_code) DO NOTHING
            """,
            (nomina, self_code, respondent_id, now_iso()),
        )
        if cur.rowcount == 1:
            status = "claimed"
        else:
            owner = conn.execute(
                "SELECT respondent_id FROM name_claims WHERE nomina = ? AND self_code = ?",
                (nomina, self_code),
            ).fetchone()
            status = "held" if owner["respondent_id"] == respondent_id else "taken"

        if status != "taken":
            conn.execute(
                "DELETE FROM name_claims WHERE respondent_id = ? AND NOT (nomina = ? AND self_code = ?)",
                (respondent_id, nomina, self_code),
            )
        return status


# --- answers ---------------------------------------------------------------


def upsert_answer(conn, respondent_id, question_id, page_index, value, time_spent_seconds=None):
    ts = now_iso()
    value_json = json.dumps(value)
    with transaction(conn):
        conn.execute(
            """
            INSERT INTO answers
                (respondent_id, question_id, page_index, value_json,
                 first_answered_at, last_updated_at, time_spent_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (respondent_id, question_id) DO UPDATE SET
                value_json = excluded.value_json,
                last_updated_at = excluded.last_updated_at,
                time_spent_seconds = COALESCE(excluded.time_spent_seconds, answers.time_spent_seconds)
            """,
            (respondent_id, question_id, page_index, value_json, ts, ts, time_spent_seconds),
        )


def set_answer_time_spent(conn, respondent_id, question_id, time_spent_seconds):
    with transaction(conn):
        conn.execute(
            """
            UPDATE answers SET time_spent_seconds = ?
            WHERE respondent_id = ? AND question_id = ?
            """,
            (time_spent_seconds, respondent_id, question_id),
        )


def get_answer_times(conn, respondent_id):
    """{question_id: seconds on that page} for one respondent."""
    rows = conn.execute(
        "SELECT question_id, time_spent_seconds FROM answers WHERE respondent_id = ?",
        (respondent_id,),
    ).fetchall()
    return {r["question_id"]: r["time_spent_seconds"] for r in rows}


# --- page visits (drive "time per answer") ----------------------------------


def open_page_visit(conn, respondent_id, page_index) -> int:
    ts = now_iso()
    with transaction(conn):
        cur = conn.execute(
            """
            INSERT INTO page_visits (respondent_id, page_index, entered_at)
            VALUES (?, ?, ?)
            """,
            (respondent_id, page_index, ts),
        )
        return cur.lastrowid


def close_page_visit(conn, visit_id, duration_seconds):
    with transaction(conn):
        conn.execute(
            "UPDATE page_visits SET left_at = ?, duration_seconds = ? WHERE id = ?",
            (now_iso(), duration_seconds, visit_id),
        )


def count_events(conn, respondent_id, event_type):
    return conn.execute(
        "SELECT COUNT(*) AS n FROM audit_log WHERE respondent_id = ? AND event_type = ?",
        (respondent_id, event_type),
    ).fetchone()["n"]


# --- rate limiting -----------------------------------------------------------


def check_and_record_rate_limit(conn, ip_hash, window_seconds, max_count) -> bool:
    """Return True if the request is allowed, False if the IP is over the limit."""
    now = datetime.now(timezone.utc)
    with transaction(conn):
        row = conn.execute(
            "SELECT window_start, count FROM rate_limit WHERE ip_hash = ?", (ip_hash,)
        ).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO rate_limit (ip_hash, window_start, count) VALUES (?, ?, 1)",
                (ip_hash, now.isoformat()),
            )
            return True

        window_start = datetime.fromisoformat(row["window_start"])
        if (now - window_start).total_seconds() > window_seconds:
            conn.execute(
                "UPDATE rate_limit SET window_start = ?, count = 1 WHERE ip_hash = ?",
                (now.isoformat(), ip_hash),
            )
            return True

        if row["count"] >= max_count:
            return False

        conn.execute(
            "UPDATE rate_limit SET count = count + 1 WHERE ip_hash = ?", (ip_hash,)
        )
        return True


def prune_rate_limit(conn, window_seconds):
    """Delete rate_limit rows whose window has already expired. The table
    otherwise grows by one row per distinct hashed IP forever."""
    cutoff = (datetime.now(timezone.utc) - timedelta(seconds=window_seconds)).isoformat()
    with transaction(conn):
        conn.execute("DELETE FROM rate_limit WHERE window_start < ?", (cutoff,))
