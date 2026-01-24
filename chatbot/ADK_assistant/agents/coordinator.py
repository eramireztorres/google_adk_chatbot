from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from ..callbacks.guardrails import before_model_guardrails
from ..callbacks.tool_gates import before_tool_guardrails
from ..callbacks.logging import after_model_log
from ..config.settings import Settings
from .rag_qa import build_rag_team
from .project_builder import build_project_refinement_loop


def build_root_agent(settings: Settings) -> LlmAgent:
    rag_team = build_rag_team(settings)
    project_team = build_project_refinement_loop(settings)

    rag_tool = AgentTool(agent=rag_team, skip_summarization=True)
    project_tool = AgentTool(agent=project_team, skip_summarization=True)

    coordinator = LlmAgent(
        name="Coordinator",
        model=settings.llm_model,
        instruction=(
            "Route user requests to the right tool. "
            "Use RagLoop for ADK documentation questions. "
            "Use ProjectRefinementLoop for project creation or code generation."
        ),
        description="Routes requests to the RAG QA team or project builder.",
        tools=[rag_tool, project_tool],
        before_model_callback=before_model_guardrails,
        before_tool_callback=before_tool_guardrails,
        after_model_callback=after_model_log,
    )

    return coordinator
