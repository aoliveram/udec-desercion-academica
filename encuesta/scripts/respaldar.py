#!/usr/bin/env python3
"""Copia de seguridad de la base de datos con la API de respaldo en línea de SQLite.

Se puede correr con la app funcionando (el modo WAL admite lecturas y
escrituras concurrentes). Pensado para programarse, por ejemplo cada hora
con cron:

    0 * * * *  cd /ruta/a/encuesta && .venv/bin/python scripts/respaldar.py
"""

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from motor import db, settings  # noqa: E402

MAX_BACKUPS_TO_KEEP = 168  # una semana de respaldos por hora


def main():
    if not settings.DB_PATH.exists():
        print(f"No hay base de datos en {settings.DB_PATH}; nada que respaldar.")
        return

    conn = db.connect()
    db.prune_rate_limit(conn, settings.RATE_LIMIT_WINDOW_SECONDS)

    backups_dir = settings.DATA_DIR / "respaldos"
    backups_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    dest_path = backups_dir / f"encuesta-{timestamp}.db"

    src = sqlite3.connect(settings.DB_PATH)
    dest = sqlite3.connect(dest_path)
    with dest:
        src.backup(dest)
    src.close()
    dest.close()
    dest_path.chmod(0o600)
    print(f"Respaldo: {settings.DB_PATH} -> {dest_path}")

    existing = sorted(backups_dir.glob("encuesta-*.db"))
    for stale in existing[:-MAX_BACKUPS_TO_KEEP]:
        stale.unlink()


if __name__ == "__main__":
    main()
