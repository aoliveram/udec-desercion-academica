import pytest

from motor import security, settings


def test_generate_token_unique_and_reasonably_long():
    a = security.generate_token()
    b = security.generate_token()
    assert a != b
    assert len(a) > 20


def test_hash_token_deterministic():
    assert security.hash_token("abc123") == security.hash_token("abc123")


def test_hash_token_differs_for_different_input():
    assert security.hash_token("a") != security.hash_token("b")


def test_hash_ip_deterministic_and_distinguishes_ips(monkeypatch, tmp_path):
    # get_ip_pepper() caches to data/.ip_pepper -- redirect it so tests
    # never touch the real project directory.
    monkeypatch.delenv("IP_HASH_PEPPER", raising=False)
    monkeypatch.setattr(settings, "DATA_DIR", tmp_path)
    monkeypatch.setattr(settings, "PEPPER_PATH", tmp_path / ".ip_pepper")

    a = security.hash_ip("1.2.3.4")
    b = security.hash_ip("1.2.3.4")
    c = security.hash_ip("5.6.7.8")
    assert a == b
    assert a != c
    assert "1.2.3.4" not in a


def test_sanitize_text_strips_control_characters():
    assert security.sanitize_text("hello\x00world") == "helloworld"


def test_sanitize_text_preserves_newlines_and_tabs():
    assert security.sanitize_text("a\nb\tc") == "a\nb\tc"


def test_sanitize_text_enforces_max_length():
    assert len(security.sanitize_text("x" * 100, max_len=10)) == 10


def test_sanitize_text_none_returns_empty_string():
    assert security.sanitize_text(None) == ""


def test_validate_choice_accepts_allowed_scalar():
    assert security.validate_choice("A", ["A", "B"]) == "A"


def test_validate_choice_rejects_disallowed_scalar():
    with pytest.raises(ValueError):
        security.validate_choice("C", ["A", "B"])


def test_validate_choice_accepts_allowed_list():
    assert security.validate_choice(["A", "B"], ["A", "B", "C"]) == ["A", "B"]


def test_validate_choice_rejects_list_with_one_disallowed_item():
    with pytest.raises(ValueError):
        security.validate_choice(["A", "Z"], ["A", "B"])


def test_validate_choice_none_is_always_allowed():
    assert security.validate_choice(None, ["A", "B"]) is None


def test_environment_overrides_secrets(monkeypatch, tmp_path):
    monkeypatch.setenv("DIRECTORIO_NOMINAS", str(tmp_path))
    assert settings.rosters_dir() == tmp_path
