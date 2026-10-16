"""Shared configuration constants and secret loading.

Every secret/path is looked up first in an environment variable named
like it in upper case (e.g. `directorio_nominas` -> `DIRECTORIO_NOMINAS`)
and then in `.streamlit/secrets.toml`. The environment wins so that the
demo, the CLI scripts and the tests can point somewhere else without
touching the collection server's secrets file.
"""

import os
import secrets as _secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "encuesta.db"
PEPPER_PATH = DATA_DIR / ".ip_pepper"
EXAMPLES_DIR = BASE_DIR / "ejemplos"


def get_secret(name):
    value = os.environ.get(name.upper())
    if value:
        return value
    try:
        import streamlit as st

        return st.secrets.get(name) or None
    except Exception:
        return None


def rosters_dir() -> Path:
    """Where the roster CSVs (`<nomina>.csv`) live.

    Defaults to `data/nominas/`, which is gitignored along with the rest of
    `data/`. Real rosters hold real names: keep them there or anywhere else
    outside a git checkout, never inside a tracked folder.
    """
    configured = get_secret("directorio_nominas")
    if configured:
        return Path(configured).expanduser()
    return DATA_DIR / "nominas"


# Whether to trust the X-Forwarded-For header for rate limiting. True only
# because the documented deployment (Cloudflare Tunnel) sits in front of a
# server bound to 127.0.0.1 -- a client can't reach it directly to forge
# the header. Set False if Streamlit's own server is ever exposed on a
# public interface directly.
TRUST_PROXY_HEADERS = True

# New-respondent throttling. A whole class typically starts from the same
# campus network (one shared public IP via NAT), so this needs to
# comfortably exceed the roster size, not just "abuse" levels.
RATE_LIMIT_WINDOW_SECONDS = 3600
RATE_LIMIT_MAX_NEW_RESPONDENTS = 150

# Below this dwell time, a page visit is flagged (not blocked) as suspiciously fast.
FAST_ANSWER_THRESHOLD_SECONDS = 1.0

# Text answers are hard-capped at this length before they ever reach the database.
MAX_TEXT_LENGTH = 2000


def get_ip_pepper() -> str:
    """Return the secret pepper used to hash respondent IPs for rate limiting.

    Prefers the `ip_hash_pepper` secret so a collection server can pin it.
    Falls back to a pepper generated once and cached in `data/.ip_pepper`,
    so a local demo works with zero configuration.
    """
    pepper = get_secret("ip_hash_pepper")
    if pepper:
        return pepper

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if PEPPER_PATH.exists():
        return PEPPER_PATH.read_text().strip()

    pepper = _secrets.token_hex(32)
    PEPPER_PATH.write_text(pepper)
    PEPPER_PATH.chmod(0o600)
    return pepper
