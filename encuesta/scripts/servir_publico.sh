#!/usr/bin/env bash
# Levanta la encuesta y un túnel rápido de Cloudflare, para UNA sesión de
# aplicación. Imprime la URL pública cuando está lista; Ctrl+C detiene todo.
#
#     scripts/servir_publico.sh
#
# Requiere cloudflared (`brew install cloudflared`). La URL es aleatoria y
# solo existe mientras corre este script: se genera una nueva antes de cada
# sesión, se comparte, y se cierra al terminar. Para una URL fija entre
# sesiones, usar un túnel con nombre y dominio propio (ver el README).
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v cloudflared >/dev/null 2>&1; then
    echo "cloudflared no está instalado. Instálalo con: brew install cloudflared" >&2
    exit 1
fi

LOG_DIR="data/logs"
mkdir -p "$LOG_DIR"

source .venv/bin/activate
streamlit run app.py --server.port 8501 > "$LOG_DIR/streamlit.log" 2>&1 &
STREAMLIT_PID=$!

TUNNEL_PID=""
cleanup() {
    [ -n "$TUNNEL_PID" ] && kill "$TUNNEL_PID" 2>/dev/null || true
    kill "$STREAMLIT_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Esperando a que el servidor local arranque..."
for _ in $(seq 1 30); do
    curl -s -o /dev/null "http://localhost:8501" && break
    sleep 0.5
done

cloudflared tunnel --url http://localhost:8501 > "$LOG_DIR/cloudflared.log" 2>&1 &
TUNNEL_PID=$!

echo "Esperando la URL pública..."
URL=""
for _ in $(seq 1 30); do
    URL=$(grep -o 'https://[a-zA-Z0-9.-]*\.trycloudflare\.com' "$LOG_DIR/cloudflared.log" | head -1 || true)
    [ -n "$URL" ] && break
    sleep 1
done

if [ -z "$URL" ]; then
    echo "No se pudo obtener la URL del túnel. Revisa $LOG_DIR/cloudflared.log" >&2
    exit 1
fi

cat <<EOF

==================================================================
  URL pública: $URL
  Agrega ?nomina=<nombre de la nómina> antes de compartirla, p. ej.:
  $URL/?nomina=cfisicas-2026
==================================================================

Ctrl+C para detener todo.
EOF

wait
