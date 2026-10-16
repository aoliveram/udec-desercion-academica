#!/usr/bin/env python3
"""Verifica que la cadena de hashes del registro de auditoría esté intacta.

Correrlo en cualquier momento, y siempre antes de confiar en una exportación:

    python scripts/verificar_integridad.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from motor import audit, db, settings  # noqa: E402


def main():
    if not settings.DB_PATH.exists():
        print(f"No hay base de datos en {settings.DB_PATH}.")
        sys.exit(1)

    conn = db.connect()
    ok, broken_id = audit.verify_chain(conn)
    row_count = conn.execute("SELECT COUNT(*) AS n FROM audit_log").fetchone()["n"]

    if ok:
        print(f"OK: registro de auditoría intacto ({row_count} eventos, cadena verificada).")
        sys.exit(0)

    print(f"ALTERACIÓN DETECTADA: la cadena se rompe en audit_log.id = {broken_id}.")
    sys.exit(1)


if __name__ == "__main__":
    main()
