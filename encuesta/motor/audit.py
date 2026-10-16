"""Append-only, hash-chained audit log.

Each row's hash covers the previous row's hash plus its own content, so editing
or deleting a historical row (outside the app, e.g. directly with `sqlite3`)
breaks the chain from that point forward. `verify_chain` recomputes it to prove
(or disprove) the database hasn't been tampered with.
"""

import hashlib
import json

from motor import db

GENESIS_HASH = "0" * 64


def _row_hash(prev_hash: str, event_type: str, created_at: str, payload_json: str) -> str:
    digest_input = f"{prev_hash}|{event_type}|{created_at}|{payload_json}".encode("utf-8")
    return hashlib.sha256(digest_input).hexdigest()


def append_event(conn, respondent_id, event_type: str, payload: dict):
    with db.transaction(conn):
        last = conn.execute(
            "SELECT row_hash FROM audit_log ORDER BY id DESC LIMIT 1"
        ).fetchone()
        prev_hash = last["row_hash"] if last else GENESIS_HASH

        created_at = db.now_iso()
        payload_json = json.dumps(payload, sort_keys=True, default=str)
        row_hash = _row_hash(prev_hash, event_type, created_at, payload_json)

        conn.execute(
            """
            INSERT INTO audit_log
                (respondent_id, event_type, payload_json, created_at, prev_hash, row_hash)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (respondent_id, event_type, payload_json, created_at, prev_hash, row_hash),
        )


def verify_chain(conn):
    """Recompute the hash chain from the start. Returns (ok, first_broken_id | None)."""
    rows = conn.execute(
        "SELECT id, event_type, payload_json, created_at, prev_hash, row_hash "
        "FROM audit_log ORDER BY id ASC"
    ).fetchall()

    expected_prev = GENESIS_HASH
    for row in rows:
        if row["prev_hash"] != expected_prev:
            return False, row["id"]
        recomputed = _row_hash(row["prev_hash"], row["event_type"], row["created_at"], row["payload_json"])
        if recomputed != row["row_hash"]:
            return False, row["id"]
        expected_prev = row["row_hash"]

    return True, None
