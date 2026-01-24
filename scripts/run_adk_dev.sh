#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHATBOT_DIR="${ROOT_DIR}/chatbot"
AGENT_DIR="${CHATBOT_DIR}/ADK_assistant"
ENV_SRC="${ROOT_DIR}/.env"
ENV_DEST="${AGENT_DIR}/.env"

if [[ -f "${ENV_SRC}" ]]; then
  cp "${ENV_SRC}" "${ENV_DEST}"
  set -a
  # shellcheck disable=SC1090
  source "${ENV_SRC}"
  set +a
else
  echo "Warning: ${ENV_SRC} not found. Continuing without copying .env."
fi

MCP_PORT="${MCP_PORT:-8001}"
ADK_WEB_PORT="${ADK_WEB_PORT:-8000}"

python "${ROOT_DIR}/rag/run_adk_mcp_server.py" --port "${MCP_PORT}" &
MCP_PID=$!

cleanup() {
  if kill -0 "${MCP_PID}" 2>/dev/null; then
    kill "${MCP_PID}"
  fi
}
trap cleanup EXIT

cd "${CHATBOT_DIR}"
ADK_LOG_LEVEL="${ADK_LOG_LEVEL:-INFO}"
adk web --log_level "${ADK_LOG_LEVEL}" --port "${ADK_WEB_PORT}" .
