import datetime as dt
import json
import threading

from motor import db


def _respondent(conn, rid, nomina="N"):
    db.create_respondent(conn, rid, f"tok-{rid}", nomina, "v1", None)


def test_connect_creates_expected_tables(conn):
    tables = {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"respondents", "answers", "page_visits", "audit_log", "name_claims", "rate_limit"} <= tables


def test_create_and_fetch_respondent_by_token(conn):
    db.create_respondent(conn, "resp-1", "tok-hash", "cfisicas", "v1", "iphash")
    row = db.get_respondent_by_token_hash(conn, "tok-hash")
    assert row["id"] == "resp-1"
    assert row["nomina"] == "cfisicas"
    assert row["instrument_version"] == "v1"
    assert row["status"] == "in_progress"


def test_unknown_token_returns_none(conn):
    assert db.get_respondent_by_token_hash(conn, "nope") is None


def test_upsert_answer_inserts_then_updates_in_place(conn):
    _respondent(conn, "r1")
    db.upsert_answer(conn, "r1", "q1", 0, "first", 1.0)
    db.upsert_answer(conn, "r1", "q1", 0, "second", 2.0)
    row = conn.execute("SELECT value_json, time_spent_seconds FROM answers WHERE question_id='q1'").fetchone()
    assert row["value_json"] == '"second"'
    assert row["time_spent_seconds"] == 2.0


def test_upsert_answer_keeps_prior_time_spent_when_new_value_is_none(conn):
    _respondent(conn, "r1")
    db.upsert_answer(conn, "r1", "q1", 0, "value", 5.0)
    db.upsert_answer(conn, "r1", "q1", 0, "value again", time_spent_seconds=None)
    assert db.get_answer_times(conn, "r1") == {"q1": 5.0}


def test_mark_completed_sets_status_and_timestamp(conn):
    _respondent(conn, "r1")
    db.mark_completed(conn, "r1")
    row = db.get_respondent_by_token_hash(conn, "tok-r1")
    assert row["status"] == "completed"
    assert row["completed_at"] is not None


def test_mark_completed_does_not_reopen_already_completed(conn):
    _respondent(conn, "r1")
    db.mark_completed(conn, "r1")
    first = db.get_respondent_by_token_hash(conn, "tok-r1")["completed_at"]
    db.mark_completed(conn, "r1")
    assert db.get_respondent_by_token_hash(conn, "tok-r1")["completed_at"] == first


def test_mark_declined_deletes_answers_and_releases_name(conn):
    _respondent(conn, "r1")
    db.claim_name(conn, "N", "7", "r1")
    db.upsert_answer(conn, "r1", "g1", 5, ["3", "4"], 2.0)
    db.save_survey_blob(conn, "r1", json.dumps({"g1": {"value": ["3", "4"]}}), "x")

    db.mark_declined(conn, "r1", "consentimiento", "No acepto")

    row = db.get_respondent_by_token_hash(conn, "tok-r1")
    assert row["status"] == "declined"
    assert json.loads(row["survey_data_json"]) == {"consentimiento": {"value": "No acepto"}}
    assert conn.execute("SELECT COUNT(*) AS n FROM answers").fetchone()["n"] == 0
    _respondent(conn, "r2")
    assert db.claim_name(conn, "N", "7", "r2") == "claimed"


def test_saving_is_refused_once_completed(conn):
    _respondent(conn, "r1")
    db.mark_completed(conn, "r1")
    db.save_survey_blob(conn, "r1", '{"x": 1}', "c")
    assert db.get_respondent_by_token_hash(conn, "tok-r1")["survey_data_json"] == "{}"


def test_get_respondents_filters_by_roster(conn):
    _respondent(conn, "r1", "A")
    _respondent(conn, "r2", "A")
    _respondent(conn, "r3", "B")
    assert {r["id"] for r in db.get_respondents(conn, "A")} == {"r1", "r2"}


def test_page_visit_open_and_close(conn):
    _respondent(conn, "r1")
    visit_id = db.open_page_visit(conn, "r1", 0)
    db.close_page_visit(conn, visit_id, 3.5)
    row = conn.execute("SELECT left_at, duration_seconds FROM page_visits WHERE id=?", (visit_id,)).fetchone()
    assert row["left_at"] is not None
    assert row["duration_seconds"] == 3.5


def test_rate_limit_allows_up_to_max_then_blocks(conn):
    for _ in range(3):
        assert db.check_and_record_rate_limit(conn, "iphash", window_seconds=3600, max_count=3)
    assert not db.check_and_record_rate_limit(conn, "iphash", window_seconds=3600, max_count=3)


def test_rate_limit_is_per_ip(conn):
    for _ in range(3):
        assert db.check_and_record_rate_limit(conn, "ip-a", window_seconds=3600, max_count=3)
    assert not db.check_and_record_rate_limit(conn, "ip-a", window_seconds=3600, max_count=3)
    assert db.check_and_record_rate_limit(conn, "ip-b", window_seconds=3600, max_count=3)


def test_rate_limit_resets_after_window_expires(conn):
    assert db.check_and_record_rate_limit(conn, "iphash", window_seconds=1, max_count=1)
    assert not db.check_and_record_rate_limit(conn, "iphash", window_seconds=1, max_count=1)

    past = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=2)).isoformat()
    conn.execute("UPDATE rate_limit SET window_start = ? WHERE ip_hash = ?", (past, "iphash"))
    conn.commit()

    assert db.check_and_record_rate_limit(conn, "iphash", window_seconds=1, max_count=1)


def test_prune_rate_limit_removes_only_expired_rows(conn):
    db.check_and_record_rate_limit(conn, "stale", window_seconds=3600, max_count=10)
    db.check_and_record_rate_limit(conn, "fresh", window_seconds=3600, max_count=10)

    past = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=7200)).isoformat()
    conn.execute("UPDATE rate_limit SET window_start = ? WHERE ip_hash = ?", (past, "stale"))
    conn.commit()

    db.prune_rate_limit(conn, window_seconds=3600)

    remaining = {r["ip_hash"] for r in conn.execute("SELECT ip_hash FROM rate_limit")}
    assert remaining == {"fresh"}


# --- name claims -----------------------------------------------------------


def test_claim_name_first_wins_second_is_rejected(conn):
    _respondent(conn, "r1")
    _respondent(conn, "r2")
    assert db.claim_name(conn, "N", "38", "r1") == "claimed"
    assert db.claim_name(conn, "N", "38", "r2") == "taken"


def test_claim_name_same_respondent_again_is_held_not_taken(conn):
    _respondent(conn, "r1")
    assert db.claim_name(conn, "N", "38", "r1") == "claimed"
    assert db.claim_name(conn, "N", "38", "r1") == "held"


def test_claim_name_switching_releases_the_previous_name(conn):
    _respondent(conn, "r1")
    _respondent(conn, "r2")
    db.claim_name(conn, "N", "38", "r1")
    assert db.claim_name(conn, "N", "5", "r1") == "claimed"
    assert db.claim_name(conn, "N", "38", "r2") == "claimed"


def test_claim_name_failed_attempt_keeps_existing_claim(conn):
    _respondent(conn, "r1")
    _respondent(conn, "r2")
    db.claim_name(conn, "N", "38", "r1")
    db.claim_name(conn, "N", "5", "r2")
    assert db.claim_name(conn, "N", "5", "r1") == "taken"
    assert db.claim_name(conn, "N", "38", "r1") == "held"


def test_claim_name_is_scoped_to_the_roster(conn):
    _respondent(conn, "r1", "A")
    _respondent(conn, "r2", "B")
    assert db.claim_name(conn, "A", "38", "r1") == "claimed"
    assert db.claim_name(conn, "B", "38", "r2") == "claimed"


def test_claim_name_concurrent_race_has_exactly_one_winner(conn):
    n = 12
    for i in range(n):
        _respondent(conn, f"r{i}")

    results = {}
    barrier = threading.Barrier(n)

    def worker(i):
        barrier.wait()  # release everyone at once
        results[i] = db.claim_name(conn, "N", "38", f"r{i}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert list(results.values()).count("claimed") == 1
    assert list(results.values()).count("taken") == n - 1
