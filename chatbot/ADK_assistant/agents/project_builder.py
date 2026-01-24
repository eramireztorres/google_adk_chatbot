from __future__ import annotations

from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent

from ..callbacks.guardrails import before_model_guardrails
from ..callbacks.tool_gates import before_tool_guardrails
from ..callbacks.logging import after_model_log, after_tool_log
from ..config.settings import Settings
from ..tools import file_tools, shell_tools, sanity_tools
from .rag_qa import build_rag_toolset


def build_project_pipeline(settings: Settings) -> SequentialAgent:
    requirements_agent = LlmAgent(
        name="RequirementsAgent",
        model=settings.llm_model,
        instruction=(
            "Extract clear project requirements from the user's request. "
            "Ask for missing critical info if needed."
        ),
        output_key="requirements",
        before_model_callback=before_model_guardrails,
        after_model_callback=after_model_log,
    )

    plan_agent = LlmAgent(
        name="PlanAgent",
        model=settings.llm_model,
        instruction=(
            "Create a concise project plan based on requirements: {requirements}. "
            "Include file structure and key ADK components."
        ),
        output_key="plan",
        before_model_callback=before_model_guardrails,
        after_model_callback=after_model_log,
    )

    code_writer_agent = LlmAgent(
        name="CodeWriterAgent",
        model=settings.llm_model,
        instruction=(
            "Generate the project files based on the plan. "
            "Use file tools to create/update files."
        ),
        tools=file_tools,
        output_key="generated_code",
        before_model_callback=before_model_guardrails,
        before_tool_callback=before_tool_guardrails,
        after_tool_callback=after_tool_log,
        after_model_callback=after_model_log,
    )

    adk_reviewer_agent = LlmAgent(
        name="ADKReviewerAgent",
        model=settings.llm_model,
        instruction=(
            "Review generated code for Google ADK correctness. "
            "Use the ADK RAG tool if needed. "
            "Return actionable feedback only."
        ),
        tools=[build_rag_toolset(settings)],
        output_key="review_comments",
        before_model_callback=before_model_guardrails,
        before_tool_callback=before_tool_guardrails,
        after_model_callback=after_model_log,
        after_tool_callback=after_tool_log,
    )

    sanity_agent = LlmAgent(
        name="CodeSanityAgent",
        model=settings.llm_model,
        instruction=(
            "Run code sanity checks on generated code. "
            "Call the code_sanity_check tool using the code from {generated_code}."
        ),
        tools=sanity_tools,
        output_key="sanity_report",
        before_model_callback=before_model_guardrails,
        before_tool_callback=before_tool_guardrails,
        after_tool_callback=after_tool_log,
    )

    pipeline = SequentialAgent(
        name="ProjectPipeline",
        sub_agents=[
            requirements_agent,
            plan_agent,
            code_writer_agent,
            adk_reviewer_agent,
            sanity_agent,
        ],
    )

    return pipeline


def build_project_refinement_loop(settings: Settings) -> LoopAgent:
    pipeline = build_project_pipeline(settings)
    return LoopAgent(
        name="ProjectRefinementLoop",
        sub_agents=[pipeline],
        max_iterations=settings.max_refine_iterations,
    )
