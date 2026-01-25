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

from google.adk.agents import SequentialAgent, LoopAgent

# Create specialized agents for planning, querying, code checking and synthesis to improve robustness and clarity

planning_agent = LlmAgent(
    name="PlanningAgent",
    model=model,
    instruction=(
        "You are a planning agent. Given a user question about Google ADK, "
        "if it contains multiple concepts, split it into 2-3 focused subqueries. "
        "Return the list of subqueries in a JSON array format. If only one concept, return single-element array."
    ),
    output_key="subqueries",
)

query_agent = LlmAgent(
    name="QueryAgent",
    model=model,
    instruction=(
        "Answer a focused query about Google ADK using the MCP RAG tool. "
        "If the user asks for code, include a Python code block. "
        "Only use ADK APIs that appear in the provided documentation. "
        "Do not invent convenience methods like agent.chat/agent.run/agent.invoke. "
        "Use the Runner/Invocation patterns shown in ADK docs for execution."
    ),
    tools=[rag_toolset],
    output_key="rag_response",
)

code_check_agent = LlmAgent(
    name="CodeCheckAgent",
    model=model,
    instruction=(
        "Inspect the RAG response for Python code blocks. For each code block, "
        "run the code snippet checker tool to validate imports and instantiation. "
        "If any check fails, respond with 'CHECK_FAILED'. Otherwise respond 'CHECK_PASSED'."
    ),
    tools=[],
    output_key="check_result",
)

synthesizer_agent = LlmAgent(
    name="SynthesizerAgent",
    model=model,
    instruction=(
        "Synthesize the final answer by combining the RAG responses to the subqueries. "
        "If code was checked and passed, include the code blocks in the answer. "
        "If code check failed, say you are retrying. "
        "Keep the answer concise and relevant."
    ),
    output_key="final_answer",
)

# Define a loop agent to allow retrying query and code check once if code check fails
rag_agent = LoopAgent(
    name="RagAgentLoop",
    sub_agents=[
        planning_agent,
        query_agent,
        code_check_agent,
        synthesizer_agent,
    ],
    max_iterations=2,
)


# 2. Define the Code Check Tool
def run_python_snippet(code: str, tool_context: ToolContext) -> Dict[str, object]:
    """
    Run a small Python snippet in the current environment to validate imports or
    simple instantiations. Avoid long-running operations.
    """
    if not code or not code.strip():
        return {"ok": False, "error": "No code provided."}

    # Limit snippet size to prevent abuse
    if len(code) > 1000:
        return {"ok": False, "error": "Code snippet too long."}

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as handle:
        handle.write(code)
        path = handle.name

    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=5,
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

# Attach code check tool explicitly only to the code_check_agent, and rag_toolset to query_agent
# But ADK does not support partial tool assignment yet - workaround by passing all tools but instructions limit tool usage

root_agent = LlmAgent(
    name="RootAgent",
    model=model,
    instruction=(
        "You are the main coordinator. Given a user query, use the RagAgentLoop workflow "
        "to plan, query, check code, and synthesize a final answer. "
        "If code check fails, the loop allows retrying once. "
        "Return only the final synthesized answer. "
        "Avoid commented-out or non-existent method calls."
    ),
    tools=[rag_tool, check_tool],
    output_key="final_answer",
)

