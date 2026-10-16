#!/usr/bin/env python3
"""Abre la encuesta en el navegador con la nómina ficticia de ejemplo.

Levanta `streamlit run app.py`, espera a que responda y abre
http://localhost:<puerto>/?nomina=ejemplo. Las nóminas se leen de
ejemplos/ (76 nombres inventados), nunca de la carpeta de nóminas reales.

Uso (desde la carpeta encuesta/):
    python scripts/demo.py
    python scripts/demo.py --puerto 8502
"""

import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

ENCUESTA_DIR = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nomina", default="ejemplo", help="nombre de un archivo <nomina>.csv en ejemplos/")
    parser.add_argument("--puerto", default="8501")
    args = parser.parse_args()

    url = f"http://localhost:{args.puerto}/?{urllib.parse.urlencode({'nomina': args.nomina})}"
    health_url = f"http://localhost:{args.puerto}/_stcore/health"

    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", args.puerto],
        cwd=ENCUESTA_DIR,
        env={**os.environ, "DIRECTORIO_NOMINAS": str(ENCUESTA_DIR / "ejemplos")},
    )

    try:
        print(f"Esperando a que el servidor arranque en el puerto {args.puerto}...")
        for _ in range(60):
            try:
                urllib.request.urlopen(health_url, timeout=1)
                break
            except (urllib.error.URLError, OSError):
                time.sleep(0.5)
        else:
            print(f"El servidor no respondió a tiempo. Ábrelo a mano:\n  {url}")
            proc.wait()
            return

        print(f"Abriendo {url}")
        webbrowser.open(url)
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        sys.exit(0)


if __name__ == "__main__":
    main()
