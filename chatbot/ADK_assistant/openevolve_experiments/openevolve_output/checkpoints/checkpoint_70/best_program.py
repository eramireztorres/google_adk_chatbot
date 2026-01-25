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
        "carefully analyze if it contains multiple distinct concepts. "
        "Split the question into 2-3 focused, concise subqueries if multiple concepts exist, "
        "and return them as a JSON array. If only one concept, return a single-element array. "
        "Return ONLY the JSON array with no extra text or explanation."
    ),
    output_key="subqueries",
)

query_agent = LlmAgent(
    name="QueryAgent",
    model=model,
    instruction=(
        "Answer a focused query about Google ADK using the MCP RAG tool. "
        "If the user requests code, include complete, runnable Python code blocks. "
        "Use only ADK APIs explicitly documented in the official docs. "
        "Do NOT invent or mention convenience methods like agent.chat, agent.run, or agent.invoke. "
        "Demonstrate usage strictly following the Runner/Invocation patterns shown in ADK documentation. "
        "Respond ONLY with the answer content and code blocks; no extra commentary."
    ),
    tools=[rag_toolset],
    output_key="rag_response",
)

code_check_agent = LlmAgent(
    name="CodeCheckAgent",
    model=model,
    instruction=(
        "Analyze the rag_response output and extract all Python code blocks. "
        "For each code block, invoke the code snippet checker tool to validate correct imports, syntax, and instantiations. "
        "If any code block fails validation, respond strictly with 'CHECK_FAILED'. "
        "If all code blocks pass, respond strictly with 'CHECK_PASSED'. "
        "Do NOT include any other text or explanation."
    ),
    tools=[],
    output_key="check_result",
)

synthesizer_agent = LlmAgent(
    name="SynthesizerAgent",
    model=model,
    instruction=(
        "Produce the final concise answer by synthesizing the rag_response content. "
        "If code check result is 'CHECK_PASSED', include all valid Python code blocks inline. "
        "If code check result is 'CHECK_FAILED', respond with a short message indicating retry due to code validation failure, "
        "but do NOT include any code blocks. "
        "Ensure the response is self-contained, user-ready, and free of internal notes."
    ),
    output_key="final_answer",
)

# Define a loop agent to retry the sequence once if code check fails
base_rag_agent = SequentialAgent(
    name="RagAgentPipeline",
    sub_agents=[planning_agent, query_agent, code_check_agent, synthesizer_agent],
    description="Pipeline: plan query, code check, synthesize",
)

rag_agent = LoopAgent(
    name="RagAgentLoop",
    sub_agents=[base_rag_agent],
    max_iterations=2,
)


# 2. Define the Code Check Tool
def run_python_snippet(code: str, tool_context: ToolContext) -> Dict[str, object]:
    """
    Run a small Python snippet in the current environment to validate imports or
    simple instantiations. Avoid long-running operations.
    Escalate early to exit LoopAgent early if validation fails.
    """
    if not code or not code.strip():
        return {"ok": False, "error": "No code provided."}

    # Sanitize code to prevent dangerous imports or calls (basic heuristic)
    restricted_keywords = ["import os", "import sys", "subprocess", "open(", "exec(", "eval("]
    for keyword in restricted_keywords:
        if keyword in code:
            tool_context.actions.escalate = True
            return {"ok": False, "error": f"Use of restricted keyword '{keyword}' in code snippet."}

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
        tool_context.actions.escalate = True
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
    if not result_payload["ok"]:
        tool_context.actions.escalate = True
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
        "You are the main coordinator agent. For each user query, invoke the RagAgentLoop workflow "
        "which plans, queries, checks code, and synthesizes a final answer. "
        "If code validation fails, retry the loop once to improve the answer. "
        "Respond ONLY with the final validated answer content. "
        "Avoid commented-out or non-existent method calls. Be concise and user-friendly."
    ),
    tools=[rag_tool, check_tool],
    output_key="final_answer",
)

