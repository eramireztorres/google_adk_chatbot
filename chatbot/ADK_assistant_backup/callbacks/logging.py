from __future__ import annotations

from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.models.llm_request import LlmRequest
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext


def after_model_log(
    *, callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"[after_model] agent={agent_name}")
    return llm_response


def before_model_log(
    *, callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"[before_model] agent={agent_name}")
    return None


def after_tool_log(
    tool: BaseTool,
    args: dict,
    tool_context: ToolContext,
    tool_response: dict,
) -> Optional[dict]:
    print(
        f"[after_tool] agent={tool_context.agent_name} tool={tool.name} args={args}"
    )
    return tool_response
