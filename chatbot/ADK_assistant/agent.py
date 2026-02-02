from __future__ import annotations

import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
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


# Default models per provider
_PROVIDER_DEFAULTS = {
    "google": "gemini-2.5-flash-lite",
    "openai": "gpt-4.1-mini",
    "ollama": "llama3",
}


def _detect_llm_provider() -> str:
    """
    Auto-detect LLM provider based on available API keys.

    Priority:
    1. Explicit ADK_LLM_PROVIDER env var
    2. If OPENAI_API_KEY is set -> openai
    3. If GOOGLE_API_KEY is set -> google
    4. Default to google (requires GOOGLE_API_KEY at runtime)
    """
    explicit = os.getenv("ADK_LLM_PROVIDER", "").strip().lower()
    if explicit in ("google", "openai", "ollama"):
        return explicit

    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GOOGLE_API_KEY"):
        return "google"
    if os.getenv("OLLAMA_API_BASE") or os.getenv("ADK_LLM_PROVIDER") == "ollama":
        return "ollama"

    # Default to google - will fail at runtime if GOOGLE_API_KEY not set
    return "google"


def _resolve_llm_model() -> str | LiteLlm:
    """Resolve LLM model based on provider detection."""
    provider = _detect_llm_provider()
    default_model = _PROVIDER_DEFAULTS.get(provider, "gemini-2.5-flash-lite")
    model = os.getenv("ADK_LLM_MODEL", default_model).strip()

    if provider == "openai":
        return LiteLlm(model=f"openai/{model}")
    if provider == "ollama":
        return LiteLlm(model=f"ollama_chat/{model}")
    # For Google, return the model name directly (ADK handles it natively)
    return model


def _rag_mcp_url() -> str:
    """Get RAG MCP URL with default port."""
    port = os.getenv("MCP_PORT", "8001")
    default_url = f"http://localhost:{port}/sse"
    return os.getenv("RAG_MCP_URL", default_url).strip()


model = _resolve_llm_model()
rag_mcp_url = _rag_mcp_url()


# --- Tool Definitions ---

# 1. RAG Toolset
rag_toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url=rag_mcp_url,
        timeout=300,
    )
)

# 2. Code Check Tool Function
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

# 3. Code Check Tool Wrapper
check_tool = FunctionTool(func=run_python_snippet)


# --- Agent Definitions ---

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
    tools=[check_tool],  # Correctly assigned tool
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

# Define a pipeline to run the agents in sequence
base_rag_agent = SequentialAgent(
    name="RagAgentPipeline",
    sub_agents=[planning_agent, query_agent, code_check_agent, synthesizer_agent],
    description="Pipeline: plan query, code check, synthesize",
)

# Define a loop agent to retry the sequence if needed
rag_agent = LoopAgent(
    name="Google_ADK_Researching",
    sub_agents=[base_rag_agent],
    max_iterations=2,
)

# Root Agent Setup
rag_tool = AgentTool(agent=rag_agent)

root_agent = LlmAgent(
    name="RootAgent",
    model=model,
    instruction="""You are an expert assistant specialized in Google Agent Development Kit (ADK).
Your primary role is to help users understand and work with Google ADK.

## When to use the RagAgentLoop tool
Use this tool when the user asks:
- Technical questions about Google ADK (agents, tools, sessions, state, callbacks, etc.)
- How to implement something with ADK
- Code examples or patterns for ADK
- Questions about ADK APIs, classes, or methods
- Troubleshooting ADK-related issues

## When NOT to use the RagAgentLoop tool
Respond directly without the tool for:
- Greetings (hello, hi, hey) - respond with a friendly greeting
- Thank yous and acknowledgments - respond politely
- Clarification questions about your previous response - use conversation history
- General conversation or small talk
- Questions clearly unrelated to Google ADK
- Follow-up questions that can be answered from the conversation context

## Guidelines
- Be conversational and friendly while remaining helpful
- For ADK questions, always use the RAG tool to provide accurate, grounded answers
- When the RAG tool returns code, include it in your response
- If code validation fails in the tool, the retry will handle it automatically
- Be concise but thorough in your responses
- If a user's follow-up question relates to a previous ADK answer, you may need to use the tool again for new technical details""",
    tools=[rag_tool],
    output_key="final_answer",
)
