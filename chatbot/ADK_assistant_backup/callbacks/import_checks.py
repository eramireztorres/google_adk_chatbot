from __future__ import annotations

import re
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.models.llm_request import LlmRequest
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from ..tools.import_check_tool import import_check

_CODE_FENCE_RE = re.compile(r"```(?:python)?\n.*?\n```", re.DOTALL)
_ADK_MARKERS = (
    "adk",
    "agent development kit",
    "mcp",
    "model context protocol",
    "toolset",
    "functiontool",
    "function tool",
    "llmagent",
    "llm agent",
)
_HOWTO_MARKERS = (
    "how to",
    "how can",
    "how do",
    "example",
    "sample",
    "demo",
    "code",
    "implement",
    "use",
    "call",
    "integrate",
    "setup",
)


def _extract_user_text(callback_context: CallbackContext, llm_request: LlmRequest) -> str:
    user_content = getattr(callback_context, "user_content", None)
    if user_content is not None:
        parts = getattr(user_content, "parts", None) or []
        text_parts = []
        for part in parts:
            piece = getattr(part, "text", None)
            if piece:
                text_parts.append(piece)
        if text_parts:
            return "\n".join(text_parts).strip()
    return ""

def _needs_code_block(user_text: str) -> bool:
    normalized = user_text.lower()
    if not any(marker in normalized for marker in _ADK_MARKERS):
        return False
    return any(marker in normalized for marker in _HOWTO_MARKERS)

def _has_code_block(text: str) -> bool:
    return bool(_CODE_FENCE_RE.search(text))


def after_model_import_check(
    *, callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    if callback_context.agent_name != "RagQueryAgent":
        return llm_response

    try:
        rag_answer = callback_context.state.get("rag_answer")
    except Exception:
        rag_answer = None

    if not rag_answer:
        return llm_response

    invocation_context = getattr(callback_context, "_invocation_context", None)
    if invocation_context is None:
        return llm_response

    tool_context = ToolContext(invocation_context)
    result = import_check(str(rag_answer), tool_context)
    try:
        callback_context.state["rag_import_check"] = result
    except Exception:
        pass
    return llm_response


def before_model_rag_critic_import_gate(
    *, callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    if callback_context.agent_name != "RagCriticAgent":
        return None

    user_text = _extract_user_text(callback_context, llm_request)
    try:
        rag_answer = callback_context.state.get("rag_answer")
    except Exception:
        rag_answer = None

    if rag_answer and _needs_code_block(user_text) and not _has_code_block(str(rag_answer)):
        refined = (
            f"{user_text}\n\n"
            "Provide a Python example and include at least one fenced code block "
            "showing the correct ADK imports and MCPToolset usage."
        ).strip()
        return LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text=refined)])
        )

    try:
        check = callback_context.state.get("rag_import_check")
    except Exception:
        check = None

    if not check:
        return None

    has_errors = bool(
        check.get("missing_modules")
        or check.get("missing_symbols")
        or check.get("errors")
        or check.get("error")
    )
    if not has_errors:
        return None

    original = _extract_user_text(callback_context, llm_request) or "Rewrite the query."
    missing_modules = check.get("missing_modules") or []
    missing_symbols = check.get("missing_symbols") or []
    missing = ", ".join(missing_modules + missing_symbols) or "unknown modules"
    refined = (
        f"{original}\n\n"
        "Ensure the Python example uses correct, existing Google ADK imports. "
        "Do NOT use `google_adk`. Prefer `google.adk` modules and MCPToolset examples "
        "from the ADK documentation. "
        f"Fix these failed imports if relevant: {missing}."
    )
    return LlmResponse(
        content=types.Content(role="model", parts=[types.Part(text=refined)])
    )
