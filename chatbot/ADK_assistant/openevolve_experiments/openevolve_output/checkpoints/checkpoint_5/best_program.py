from __future__ import annotations

import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from google.adk.tools.tool_context import ToolContext

load_dotenv()


def _configure_logging() -> None:
    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "adk.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


_configure_logging()



# Validating and resolving configuration
def _resolve_llm_model() -> str | LiteLlm:
    provider = os.getenv("ADK_LLM_PROVIDER", "openai").strip().lower()
    model = os.getenv("ADK_LLM_MODEL", "gpt-4.1-mini").strip()
    if provider == "openai":
        return LiteLlm(model=f"openai/{model}")
    return model

def _rag_mcp_url() -> str:
    return os.getenv("RAG_MCP_URL", "http://127.0.0.1:8000/sse").strip()

model = _resolve_llm_model()
rag_mcp_url = _rag_mcp_url()

# 1. Define the RAG Agent
rag_toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url=rag_mcp_url,
        timeout=300,
    )
)

rag_agent = LlmAgent(
    name="RagAgent",
    model=model,
    instruction=(
        "Answer user questions about Google ADK using the MCP RAG tool. "
        "If the question has multiple concepts, split into 2-3 focused subqueries, "
        "call the MCP tool for each, and synthesize a single answer. "
        "If the user asks for code, include a Python code block. "
        "Only use ADK APIs that appear in the provided documentation. "
        "Do not invent convenience methods like agent.chat/agent.run/agent.invoke. "
        "Use the Runner/Invocation patterns shown in ADK docs for execution. "
        "Do not include commented-out calls to non-existent methods; omit the call entirely."
    ),
    tools=[rag_toolset],
)


# 2. Define the Code Check Tool
def run_python_snippet(code: str, tool_context: ToolContext) -> Dict[str, object]:
    """
    Run a small Python snippet in the current environment to validate imports or
    simple instantiations. Avoid long-running operations.
    """
    if not code or not code.strip():
        return {"ok": False, "error": "No code provided."}

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as handle:
        handle.write(code)
        path = handle.name

    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Execution timed out."}
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass

    result_payload = {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
    return result_payload


# 3. Define the Root Agent
rag_tool = AgentTool(agent=rag_agent)
check_tool = FunctionTool(func=run_python_snippet)

root_agent = LlmAgent(
    name="RootAgent",
    model=model,
    instruction=(
        "You are the main coordinator. For every user query, call the RAG tool. "
        "If the RagAgent response includes a Python code block, run a minimal "
        "import/instantiation check using the code-check tool before responding. "
        "If the check fails, reformulate the query and call the RAG tool again, "
        "then re-check once before responding. "
        "Do not return commented-out calls to non-existent methods."
    ),
    tools=[rag_tool, check_tool],
)

