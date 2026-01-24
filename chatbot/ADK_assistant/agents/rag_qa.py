from __future__ import annotations

from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

from ..callbacks.guardrails import before_model_guardrails
from ..callbacks.tool_gates import before_tool_guardrails
from ..callbacks.logging import after_model_log, after_tool_log
from ..config.settings import Settings

def build_rag_toolset(settings: Settings) -> MCPToolset:
    return MCPToolset(
        connection_params=SseConnectionParams(
            url=settings.rag_mcp_url,
            timeout=300,
        )
    )


def build_rag_team(settings: Settings) -> LoopAgent:
    rag_toolset = build_rag_toolset(settings)

    rag_query_agent = LlmAgent(
        name="RagQueryAgent",
        model=settings.llm_model,
        instruction=(
            "Answer the user using the ADK documentation via the MCP tool. "
            "If needed, call the tool to retrieve context."
        ),
        tools=[rag_toolset],
        output_key="rag_answer",
        before_model_callback=before_model_guardrails,
        before_tool_callback=before_tool_guardrails,
        after_model_callback=after_model_log,
        after_tool_callback=after_tool_log,
    )

    rag_critic_agent = LlmAgent(
        name="RagCriticAgent",
        model=settings.llm_model,
        instruction=(
            "Review the current answer: {rag_answer}. "
            "If it is incomplete, rewrite the user query to be more specific. "
            "If it is sufficient, return the original query unchanged. "
            "Output ONLY the improved query text."
        ),
        output_key="rag_query",
        before_model_callback=before_model_guardrails,
    )

    return LoopAgent(
        name="RagLoop",
        sub_agents=[rag_query_agent, rag_critic_agent],
        max_iterations=settings.max_rag_iterations,
    )
