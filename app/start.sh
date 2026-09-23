echo "Checking PostgreSQL..."
if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
  echo "Postgres not ready. Trying brew services start..."
  brew services start postgresql@14 2>/dev/null \
    || brew services start postgresql@14 2>/dev/null \
    || brew services start postgresql 2>/dev/null \
    || true
  sleep 2
fi

if pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
  echo "PostgreSQL is ready."
else
  echo "WARNING: PostgreSQL is not ready. API may fail on DB writes."
fi

#!/usr/bin/env bash
set -euo pipefail

# корень app/ (где лежит этот скрипт)
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$APP_DIR"

# venv: Trump/venv относительно app/
VENV_DIR="${APP_DIR}/../venv"
if [[ ! -d "$VENV_DIR" ]]; then
  echo "venv not found at: $VENV_DIR"
  exit 1
fi

# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

FRONTEND_DIR="${APP_DIR}/frontend"
if [[ ! -d "$FRONTEND_DIR" ]]; then
  echo "frontend not found at: $FRONTEND_DIR"
  exit 1
fi

API_HOST="${API_HOST:-0.0.0.0}"
API_PORT="${API_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

cleanup() {
  echo ""
  echo "Stopping..."
  if [[ -n "${API_PID:-}" ]] && kill -0 "$API_PID" 2>/dev/null; then
    kill "$API_PID" 2>/dev/null || true
  fi
  if [[ -n "${WEB_PID:-}" ]] && kill -0 "$WEB_PID" 2>/dev/null; then
    kill "$WEB_PID" 2>/dev/null || true
  fi
  wait 2>/dev/null || true
  echo "Stopped."
}

trap cleanup EXIT INT TERM

echo "Starting API  →  http://127.0.0.1:${API_PORT}  (docs: /docs)"
(
  cd "$APP_DIR"
  uvicorn api.app:app --reload --host "$API_HOST" --port "$API_PORT"
) &
API_PID=$!

echo "Starting Web  →  http://127.0.0.1:${FRONTEND_PORT}"
(
  cd "$FRONTEND_DIR"
  npm run dev -- --host 127.0.0.1 --port "$FRONTEND_PORT"
) &
WEB_PID=$!

echo ""
echo "Both started. Press Ctrl+C to stop."
echo "  API PID: $API_PID"
echo "  WEB PID: $WEB_PID"
echo ""

# ждём любой из процессов; если один упал — выходим и сработает cleanup
wait -n "$API_PID" "$WEB_PID" 2>/dev/null || wait