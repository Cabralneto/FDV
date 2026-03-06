#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
RUNTIME_DIR="$ROOT_DIR/.runtime"
mkdir -p "$RUNTIME_DIR"

BACKEND_PID_FILE="$RUNTIME_DIR/backend.pid"
FRONTEND_PID_FILE="$RUNTIME_DIR/frontend.pid"
BACKEND_LOG="$RUNTIME_DIR/backend.log"
FRONTEND_LOG="$RUNTIME_DIR/frontend.log"

wait_for_url() {
  local url="$1"
  local max_attempts="${2:-60}"
  local attempt=1
  until curl -fsS "$url" >/dev/null 2>&1; do
    if [ "$attempt" -ge "$max_attempts" ]; then
      echo "[ERRO] Timeout aguardando $url"
      return 1
    fi
    attempt=$((attempt + 1))
    sleep 1
  done
}

copy_env_if_missing() {
  local example="$1"
  local target="$2"
  if [ ! -f "$target" ]; then
    cp "$example" "$target"
    echo "[INFO] Criado $target a partir de $example"
  fi
}

start_postgres() {
  if command -v docker >/dev/null 2>&1; then
    echo "[INFO] Subindo Postgres com Docker..."
    (cd "$ROOT_DIR" && docker compose up -d postgres)
    echo "[INFO] Aguardando Postgres ficar pronto..."
    (cd "$ROOT_DIR" && docker compose exec -T postgres pg_isready -U portal -d portal_obra >/dev/null)
  else
    echo "[WARN] Docker não encontrado. Assumindo PostgreSQL local já disponível em localhost:5432"
  fi
}

setup_backend() {
  echo "[INFO] Configurando backend..."
  copy_env_if_missing "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"

  if [ ! -d "$BACKEND_DIR/.venv" ]; then
    python3 -m venv "$BACKEND_DIR/.venv"
  fi

  # shellcheck disable=SC1091
  source "$BACKEND_DIR/.venv/bin/activate"
  pip install --upgrade pip >/dev/null
  pip install -r "$BACKEND_DIR/requirements.txt"

  set -a
  # shellcheck disable=SC1090
  source "$BACKEND_DIR/.env"
  set +a

  if [ -f "$BACKEND_PID_FILE" ] && kill -0 "$(cat "$BACKEND_PID_FILE")" 2>/dev/null; then
    echo "[INFO] Backend já está rodando (PID $(cat "$BACKEND_PID_FILE"))"
  else
    echo "[INFO] Iniciando backend..."
    nohup "$BACKEND_DIR/.venv/bin/uvicorn" app.main:app --host 0.0.0.0 --port 8000 --app-dir "$BACKEND_DIR" >"$BACKEND_LOG" 2>&1 &
    echo $! > "$BACKEND_PID_FILE"
  fi

  wait_for_url "http://localhost:8000/health" 90
  echo "[INFO] Aplicando seed..."
  python "$BACKEND_DIR/scripts_seed.py"
  deactivate
}

setup_frontend() {
  echo "[INFO] Configurando frontend..."
  copy_env_if_missing "$FRONTEND_DIR/.env.example" "$FRONTEND_DIR/.env.local"

  (cd "$FRONTEND_DIR" && npm install)

  if [ -f "$FRONTEND_PID_FILE" ] && kill -0 "$(cat "$FRONTEND_PID_FILE")" 2>/dev/null; then
    echo "[INFO] Frontend já está rodando (PID $(cat "$FRONTEND_PID_FILE"))"
  else
    echo "[INFO] Iniciando frontend..."
    (cd "$FRONTEND_DIR" && nohup npm run dev -- --hostname 0.0.0.0 --port 3000 >"$FRONTEND_LOG" 2>&1 & echo $! > "$FRONTEND_PID_FILE")
  fi

  wait_for_url "http://localhost:3000" 120
}

stop_services() {
  if [ -f "$BACKEND_PID_FILE" ] && kill -0 "$(cat "$BACKEND_PID_FILE")" 2>/dev/null; then
    kill "$(cat "$BACKEND_PID_FILE")" || true
    rm -f "$BACKEND_PID_FILE"
    echo "[INFO] Backend parado"
  fi

  if [ -f "$FRONTEND_PID_FILE" ] && kill -0 "$(cat "$FRONTEND_PID_FILE")" 2>/dev/null; then
    kill "$(cat "$FRONTEND_PID_FILE")" || true
    rm -f "$FRONTEND_PID_FILE"
    echo "[INFO] Frontend parado"
  fi

  if command -v docker >/dev/null 2>&1; then
    (cd "$ROOT_DIR" && docker compose stop postgres >/dev/null || true)
    echo "[INFO] Postgres parado"
  fi
}

command="${1:-start}"
case "$command" in
  start)
    start_postgres
    setup_backend
    setup_frontend
    echo ""
    echo "✅ Portal da Obra disponível em: http://localhost:3000"
    echo "✅ API disponível em: http://localhost:8000/docs"
    echo "📄 Logs backend: $BACKEND_LOG"
    echo "📄 Logs frontend: $FRONTEND_LOG"
    ;;
  stop)
    stop_services
    ;;
  restart)
    stop_services
    start_postgres
    setup_backend
    setup_frontend
    ;;
  *)
    echo "Uso: $0 [start|stop|restart]"
    exit 1
    ;;
esac
