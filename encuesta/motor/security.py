"""Token handling and input validation.

Kept free of Streamlit and database imports so it can be unit-tested and reused
by the standalone scripts without pulling in the app runtime.
"""

import hashlib
import secrets
import unicodedata

from motor import settings


def generate_token() -> str:
    """A high-entropy, URL-safe token handed to the respondent for resuming."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """One-way hash used to look up a respondent by token without storing it in plaintext."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def hash_ip(ip_address: str) -> str:
    """Salted hash of a client IP, used only for rate-limit counting (never stored raw)."""
    pepper = settings.get_ip_pepper()
    return hashlib.sha256(f"{pepper}:{ip_address}".encode("utf-8")).hexdigest()


def sanitize_text(value: str, max_len: int = settings.MAX_TEXT_LENGTH) -> str:
    """Strip control characters and enforce a max length before text reaches the database."""
    if value is None:
        return ""
    cleaned = "".join(
        ch for ch in value if ch in ("\n", "\t") or unicodedata.category(ch)[0] != "C"
    )
    return cleaned.strip()[:max_len]


def validate_choice(value, allowed_options):
    """Reject a value outside a question's declared option set.

    Widget option lists are enforced client-side only, so a tampered or replayed
    session_state value could otherwise smuggle in an out-of-band answer.
    """
    if isinstance(value, (list, tuple, set)):
        for item in value:
            if item not in allowed_options:
                raise ValueError(f"Value {item!r} is not an allowed option")
        return value
    if value is not None and value not in allowed_options:
        raise ValueError(f"Value {value!r} is not an allowed option")
    return value
