import threading

from motor import audit


def test_append_and_verify_chain_intact(conn):
    audit.append_event(conn, "r1", "event_a", {"x": 1})
    audit.append_event(conn, "r1", "event_b", {"x": 2})
    ok, broken_id = audit.verify_chain(conn)
    assert ok
    assert broken_id is None


def test_chain_links_to_genesis_on_first_row(conn):
    audit.append_event(conn, "r1", "event_a", {})
    row = conn.execute("SELECT prev_hash FROM audit_log ORDER BY id LIMIT 1").fetchone()
    assert row["prev_hash"] == audit.GENESIS_HASH


def test_verify_chain_detects_tampered_payload(conn):
    audit.append_event(conn, "r1", "event_a", {"x": 1})
    audit.append_event(conn, "r1", "event_b", {"x": 2})
    conn.execute("UPDATE audit_log SET payload_json = ? WHERE event_type = 'event_a'", ('{"x": 999}',))
    conn.commit()

    ok, broken_id = audit.verify_chain(conn)
    assert not ok
    assert broken_id is not None


def test_verify_chain_detects_deleted_row(conn):
    audit.append_event(conn, "r1", "event_a", {})
    audit.append_event(conn, "r1", "event_b", {})
    audit.append_event(conn, "r1", "event_c", {})
    conn.execute("DELETE FROM audit_log WHERE event_type = 'event_b'")
    conn.commit()

    ok, _ = audit.verify_chain(conn)
    assert not ok


def test_empty_log_is_valid(conn):
    ok, broken_id = audit.verify_chain(conn)
    assert ok
    assert broken_id is None


def test_concurrent_appends_do_not_fork_the_chain(conn):
    """Regression test for the race db.transaction()'s write lock fixes:
    without it, two threads could both read the same last row_hash and
    each insert a row chained to that same parent, and verify_chain()
    would then report tampering that never happened."""
    n_threads = 8
    n_events_per_thread = 20

    def worker(i):
        for j in range(n_events_per_thread):
            audit.append_event(conn, f"r{i}", "concurrent_event", {"thread": i, "n": j})

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    count = conn.execute("SELECT COUNT(*) AS n FROM audit_log").fetchone()["n"]
    assert count == n_threads * n_events_per_thread

    ok, broken_id = audit.verify_chain(conn)
    assert ok, f"chain broken at audit_log.id={broken_id}"
