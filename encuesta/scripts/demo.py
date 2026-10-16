#!/usr/bin/env python3
"""Abre la encuesta en el navegador con la nómina ficticia de ejemplo.

Levanta `streamlit run app.py`, espera a que responda y abre
http://localhost:<puerto>/?nomina=ejemplo. Las nóminas se leen de
ejemplos/ (76 nombres inventados), nunca de la carpeta de nóminas reales.

Uso (desde cualquier carpeta):
    python scripts/demo.py
    python scripts/demo.py --puerto 8502

Sin --puerto usa el primer puerto libre desde 8501, así no choca con otra
app de Streamlit que ya esté corriendo.
"""

import argparse
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

ENCUESTA_DIR = Path(__file__).resolve().parent.parent


def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def first_free_port(start=8501, tries=50):
    return next(str(p) for p in range(start, start + tries) if port_is_free(p))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nomina", default="ejemplo", help="nombre de un archivo <nomina>.csv en ejemplos/")
    parser.add_argument("--puerto", help="por defecto, el primer puerto libre desde 8501")
    args = parser.parse_args()

    if args.puerto is None:
        args.puerto = first_free_port()
    elif not port_is_free(int(args.puerto)):
        sys.exit(f"El puerto {args.puerto} está ocupado por otra aplicación. Prueba sin --puerto.")

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
            if proc.poll() is not None:
                sys.exit("El servidor de la encuesta se cerró al arrancar; revisa el mensaje de arriba.")
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
