#!/bin/bash
set -e

# Configuration
MCP_SERVER_SCRIPT="/home/erick/repo/google_adk_chatbot/rag/run_adk_mcp_server.py"
INITIAL_PROGRAM="/home/erick/repo/google_adk_chatbot/chatbot/ADK_assistant/openevolve_experiments/initial_program.py"
EVALUATOR="/home/erick/repo/google_adk_chatbot/chatbot/ADK_assistant/openevolve_experiments/evaluator.py"
CONFIG="/home/erick/repo/google_adk_chatbot/chatbot/ADK_assistant/openevolve_experiments/config.yaml"
VENV_PYTHON="/home/erick/repo/google_adk_chatbot/venv/bin/python"
OPENEVOLVE_RUN="/home/erick/repo/google_adk_chatbot/venv/bin/openevolve-run"
RAG_MCP_URL="http://127.0.0.1:8000/sse"

# Start MCP Server
echo "Starting MCP Server..."
$VENV_PYTHON $MCP_SERVER_SCRIPT --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Function to kill server on exit
cleanup() {
    echo "Stopping MCP Server (PID $SERVER_PID)..."
    kill $SERVER_PID
}
trap cleanup EXIT

# Wait for server to be ready
echo "Waiting for MCP Server to be ready at $RAG_MCP_URL..."
timeout=30
elapsed=0
while ! curl -s $RAG_MCP_URL > /dev/null; do
    sleep 1
    elapsed=$((elapsed+1))
    if [ $elapsed -ge $timeout ]; then
        echo "Error: MCP Server failed to start within $timeout seconds."
        exit 1
    fi
done
echo "MCP Server is up!"

# Run OpenEvolve
echo "Running OpenEvolve..."
$OPENEVOLVE_RUN "$INITIAL_PROGRAM" "$EVALUATOR" --config "$CONFIG" --iterations 1

echo "Experiment finished."
