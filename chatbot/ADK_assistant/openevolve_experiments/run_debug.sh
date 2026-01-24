#!/bin/bash
set -e

# Configuration
VENV_PYTHON="/home/erick/repo/google_adk_chatbot/venv/bin/python"
MCP_SERVER_SCRIPT="/home/erick/repo/google_adk_chatbot/rag/run_adk_mcp_server.py"
DEBUG_SCRIPT="/home/erick/repo/google_adk_chatbot/chatbot/ADK_assistant/openevolve_experiments/debug_evaluator.py"
RAG_MCP_URL="http://127.0.0.1:8000/sse"

echo "=== Starting Debug Session ==="

# 1. Start MCP Server
echo "Starting MCP Server (host=127.0.0.1, port=8000)..."
$VENV_PYTHON $MCP_SERVER_SCRIPT --host 127.0.0.1 --port 8000 > /tmp/mcp_server.log 2>&1 &
SERVER_PID=$!
echo "MCP Server PID: $SERVER_PID"

# Cleanup function
cleanup() {
    echo "Stopping MCP Server (PID $SERVER_PID)..."
    kill $SERVER_PID
    # echo "Server Log Tail:"
    # tail -n 20 /tmp/mcp_server.log
}
trap cleanup EXIT

# 2. Wait for server
echo "Waiting for MCP Server..."
timeout=10
elapsed=0
while true; do
    set +e
    curl -s --max-time 1 $RAG_MCP_URL > /dev/null
    RET=$?
    set -e
    if [ $RET -eq 0 ] || [ $RET -eq 28 ]; then
        break
    fi
    sleep 1
    elapsed=$((elapsed+1))
    if [ $elapsed -ge $timeout ]; then
        echo "Authentication/Connection check failed or timed out (Exit code: $RET)."
        # We don't exit here, we verify connectivity, but curl might fail 404 or something which is fine for connectivity check
        # But actually 200 OK is expected for GET /sse? No, usually 200 OK.
        # Let's check logs
        cat /tmp/mcp_server.log
        exit 1
    fi
done
echo "MCP Server is reachable."

# 3. Run Debug Script
echo "Running debug_evaluator.py..."
$VENV_PYTHON $DEBUG_SCRIPT

echo "=== Debug Session Finished ==="
