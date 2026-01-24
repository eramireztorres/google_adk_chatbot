from __future__ import annotations

from typing import AsyncGenerator

from google.adk.agents import LlmAgent, LoopAgent
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from google.genai import types

from ..callbacks.routing_guardrails import before_model_routing_guardrails
from ..callbacks.tool_gates import before_tool_guardrails
from ..callbacks.logging import after_model_log, after_tool_log
from ..callbacks.import_checks import (
    after_model_import_check,
    before_model_rag_critic_import_gate,
)
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
            "If the query contains multiple distinct concepts, split it into "
            "2-3 focused subqueries, call the MCP tool for each, and synthesize "
            "a single Python-focused answer grounded in the retrieved context. "
            "Always include a Python code block when the user asks for code."
        ),
        include_contents="none",
        tools=[rag_toolset],
        output_key="rag_answer",
        before_model_callback=before_model_routing_guardrails,
        before_tool_callback=before_tool_guardrails,
        after_model_callback=[after_model_log, after_model_import_check],
        after_tool_callback=after_tool_log,
    )

    rag_critic_agent = LlmAgent(
        name="RagCriticAgent",
        model=settings.llm_model,
        instruction=(
            "Review the current answer: {rag_answer}. "
            "If it is incomplete, rewrite the user query to be more specific. "
            "If the question mixes multiple concepts, split into 2-3 short subqueries "
            "separated by newlines. "
            "If it is sufficient, return the original query unchanged. "
            "Keep the user's intent and language; do not switch languages or platforms. "
            "Output ONLY the improved query text."
        ),
        include_contents="none",
        output_key="rag_query",
        before_model_callback=[before_model_routing_guardrails, before_model_rag_critic_import_gate],
    )

    class StopIfRagStable(BaseAgent):
        async def _run_async_impl(
            self, ctx: InvocationContext
        ) -> AsyncGenerator[Event, None]:
            rag_query = ctx.session.state.get("rag_query")
            rag_query_prev = ctx.session.state.get("rag_query_prev")
            rag_answer = ctx.session.state.get("rag_answer")
            import_check = ctx.session.state.get("rag_import_check") or {}

            import_ok = bool(import_check) and bool(import_check.get("ok"))
            stop_for_stability = bool(
                import_ok and rag_query and rag_query_prev and rag_query == rag_query_prev
            )
            stop_for_imports = bool(import_ok and rag_answer)

            if rag_query:
                ctx.session.state["rag_query_prev"] = rag_query

            should_stop = stop_for_stability or stop_for_imports
            print(
                "[StopIfRagStable] stop=%s stability=%s import_ok=%s has_answer=%s"
                % (should_stop, stop_for_stability, import_ok, bool(rag_answer))
            )
            yield Event(author=self.name, actions=EventActions(escalate=should_stop))

    def _finalize_rag_loop(callback_context: CallbackContext) -> types.Content | None:
        rag_answer = None
        try:
            rag_answer = callback_context.state.get("rag_answer")
        except Exception:
            rag_answer = None

        try:
            import_check = callback_context.state.get("rag_import_check")
        except Exception:
            import_check = None

        if import_check:
            missing = import_check.get("missing_modules") or []
            errors = import_check.get("errors") or []
            check_error = import_check.get("error")
            if missing or errors or check_error:
                details = []
                if check_error:
                    details.append(f"Error: {check_error}")
                if missing:
                    details.append(f"Missing modules: {', '.join(missing)}")
                if errors:
                    details.append("Import errors: " + "; ".join(errors))
                detail_text = "\n".join(details) if details else "Unknown import failure."
                message = (
                    "I couldn't produce a verified Python example because the code "
                    "fails import checks after multiple attempts.\n\n"
                    f"{detail_text}\n\n"
                    "Please confirm your target environment and required packages, "
                    "or specify the exact ADK version and tooling you want to use."
                )
                return types.Content(role="model", parts=[types.Part(text=message)])
        if rag_answer:
            return types.Content(role="model", parts=[types.Part(text=rag_answer)])
        rag_query = None
        try:
            rag_query = callback_context.state.get("rag_query")
        except Exception:
            rag_query = None
        if rag_query:
            return types.Content(role="model", parts=[types.Part(text=rag_query)])
        return None

    return LoopAgent(
        name="RagLoop",
        sub_agents=[rag_query_agent, rag_critic_agent, StopIfRagStable(name="StopIfRagStable")],
        max_iterations=settings.max_rag_iterations,
        after_agent_callback=_finalize_rag_loop,
    )
