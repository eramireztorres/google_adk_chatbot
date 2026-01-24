from __future__ import annotations

import json
from typing import AsyncGenerator, Literal, Optional

from pydantic import BaseModel, Field

from google.adk.agents import BaseAgent, LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai import types

from ..callbacks.routing_guardrails import _is_prompt_injection
from ..config.settings import Settings
from .rag_qa import build_rag_team
from .project_builder import build_project_refinement_loop


class RouteDecision(BaseModel):
    route: Literal["rag", "project", "smalltalk"] = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str = Field(...)


def _extract_user_text(content: Optional[types.Content]) -> str:
    if content is None or not content.parts:
        return ""
    parts = []
    for part in content.parts:
        if part.text:
            parts.append(part.text)
    return "\n".join(parts).strip()


def _parse_route(raw: object) -> RouteDecision:
    if isinstance(raw, RouteDecision):
        return raw
    if isinstance(raw, dict):
        try:
            return RouteDecision(**raw)
        except Exception:
            return RouteDecision(route="rag", confidence=0.0, reason="fallback")
    if isinstance(raw, str) and raw:
        try:
            return RouteDecision(**json.loads(raw))
        except json.JSONDecodeError:
            return RouteDecision(route="rag", confidence=0.0, reason="fallback")
    return RouteDecision(route="rag", confidence=0.0, reason="fallback")


def _build_rag_response(ctx: InvocationContext) -> types.Content:
    rag_answer = ctx.session.state.get("rag_answer")
    import_check = ctx.session.state.get("rag_import_check") or {}

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
        return types.Content(role="model", parts=[types.Part(text=str(rag_answer))])

    return types.Content(
        role="model",
        parts=[
            types.Part(
                text="I couldn't retrieve a reliable answer. Please clarify your request."
            )
        ],
    )


class RoutingCoordinator(BaseAgent):
    def __init__(
        self,
        *,
        settings: Settings,
        router: LlmAgent,
        rag_team: BaseAgent,
        project_team: BaseAgent,
        smalltalk_agent: LlmAgent,
        project_summary_agent: LlmAgent,
    ) -> None:
        super().__init__(
            name="Coordinator",
            description="Routes requests and returns final answers.",
            sub_agents=[router, rag_team, project_team, smalltalk_agent, project_summary_agent],
        )
        self._settings = settings
        self._router = router
        self._rag_team = rag_team
        self._project_team = project_team
        self._smalltalk_agent = smalltalk_agent
        self._project_summary_agent = project_summary_agent

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        user_text = _extract_user_text(ctx.user_content).lower()
        if user_text and _is_prompt_injection(user_text):
            yield Event(
                author=self.name,
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text="I can't follow that request. Please rephrase your question about Google ADK."
                        )
                    ],
                ),
                actions=EventActions(skip_summarization=True),
            )
            return

        async for _ in self._router.run_async(ctx):
            pass

        decision = _parse_route(ctx.session.state.get("route_decision"))
        route = decision.route or "rag"

        if route == "project":
            async for _ in self._project_team.run_async(ctx):
                pass
            async for event in self._project_summary_agent.run_async(ctx):
                yield event
            return

        if route == "smalltalk":
            async for event in self._smalltalk_agent.run_async(ctx):
                yield event
            return

        async for _ in self._rag_team.run_async(ctx):
            pass
        rag_content = _build_rag_response(ctx)
        yield Event(
            author=self.name,
            content=rag_content,
            actions=EventActions(skip_summarization=True),
        )


def build_root_agent(settings: Settings) -> BaseAgent:
    router = LlmAgent(
        name="CoordinatorRouter",
        model=settings.llm_model,
        instruction=(
            "Classify the user's intent and output JSON for RouteDecision. "
            "Use route='project' for requests to create/generate/modify a project or files. "
            "Use route='rag' for ADK/MCP/A2A questions, API usage, and code examples. "
            "Use route='smalltalk' for greetings or non-ADK chit-chat. "
            "Default to route='rag' if unsure."
        ),
        output_schema=RouteDecision,
        output_key="route_decision",
        include_contents="none",
    )

    rag_team = build_rag_team(settings)
    project_team = build_project_refinement_loop(settings)

    smalltalk_agent = LlmAgent(
        name="SmalltalkAgent",
        model=settings.llm_model,
        instruction=(
            "Reply briefly and politely. "
            "If the user asks about Google ADK, say you'll look it up in the docs."
        ),
    )

    project_summary_agent = LlmAgent(
        name="ProjectSummaryAgent",
        model=settings.llm_model,
        instruction=(
            "Summarize the project work using state: requirements, plan, "
            "review_comments, sanity_report. "
            "Do not invent files or APIs. "
            "If key details are missing, ask a clarifying question."
        ),
    )

    return RoutingCoordinator(
        settings=settings,
        router=router,
        rag_team=rag_team,
        project_team=project_team,
        smalltalk_agent=smalltalk_agent,
        project_summary_agent=project_summary_agent,
    )
