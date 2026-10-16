"""Rosters ("nóminas"): who can answer and who can be nominated.

Each roster is a CSV at `<settings.rosters_dir()>/<nomina>.csv` with:

- `N`       stable per-person code. Nominations are stored by this code,
            never by name, and pseudonyms at export are derived from it --
            keep it the same across waves for the same person.
- `NOMBRE`  the name shown on screen.
- `COHORTE` optional; when present, nomination lists are grouped by it.

Excel's "CSV UTF-8" export (with BOM) and the `;` separator Excel uses in
Spanish locales are both accepted. Plain Python (no Streamlit imports), so
the app, the export script and the tests all read rosters the same way.
"""

import csv
import re
import unicodedata
from collections import namedtuple
from pathlib import Path

from motor import settings

Person = namedtuple("Person", "code name cohort")

_NOMINA_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


class RosterError(ValueError):
    """The roster file exists but can't be used as is."""


def roster_path(nomina, base_dir=None):
    """Path of a roster's CSV, or None if `nomina` doesn't look like a plain
    file name (it comes straight from the URL query string)."""
    if not nomina or not _NOMINA_RE.match(nomina):
        return None
    base = Path(base_dir or settings.rosters_dir()).resolve()
    path = (base / f"{nomina}.csv").resolve()
    if path.parent != base:
        return None
    return path


def read_roster(path):
    """[Person, ...] in file order. Raises RosterError on a malformed file."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        text = f.read()
    first_line = text.split("\n", 1)[0]
    delimiter = ";" if first_line.count(";") > first_line.count(",") else ","
    rows = list(csv.DictReader(text.splitlines(), delimiter=delimiter))

    if not rows:
        raise RosterError(f"{path.name}: la nómina está vacía")
    header = {(h or "").strip().upper() for h in rows[0].keys()}
    for required in ("N", "NOMBRE"):
        if required not in header:
            raise RosterError(f"{path.name}: falta la columna {required}")

    people = []
    seen = set()
    for i, row in enumerate(rows, start=2):
        row = {(k or "").strip().upper(): (v or "").strip() for k, v in row.items()}
        code, name = row["N"], row["NOMBRE"]
        if not code and not name:
            continue  # blank line left by a spreadsheet
        if not code or not name:
            raise RosterError(f"{path.name}, fila {i}: N y NOMBRE no pueden quedar vacíos")
        if code in seen:
            raise RosterError(f"{path.name}, fila {i}: el código N={code} está repetido")
        seen.add(code)
        people.append(Person(code, name, row.get("COHORTE", "")))
    return people


def load_roster(nomina, base_dir=None):
    """[Person, ...] for a roster name, or None if there's no such roster."""
    path = roster_path(nomina, base_dir)
    if path is None or not path.exists():
        return None
    return read_roster(path)


def normalize(text):
    """Lowercase, accent-insensitive form used by the name filter."""
    decomposed = unicodedata.normalize("NFKD", text or "")
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).casefold()


def display_order(people):
    """People sorted by cohort and then by name, the order used on screen."""
    return sorted(people, key=lambda p: (p.cohort, normalize(p.name)))


def has_cohorts(people):
    return len({p.cohort for p in people}) > 1
