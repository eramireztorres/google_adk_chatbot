from __future__ import annotations

from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types


_DEFAULT_BLOCK_MESSAGE = (
    "I can't follow that request. Please rephrase your question about Google ADK."
)

_BLOCK_PATTERNS = [
    "ignore previous",
    "system prompt",
    "developer message",
    "act as",
    "pretend to be",
    "jailbreak",
]


def _extract_text(llm_request: LlmRequest) -> str:
    text_parts = []
    contents = getattr(llm_request, "contents", None)
    if contents:
        for content in contents:
            parts = getattr(content, "parts", None) or []
            for part in parts:
                piece = getattr(part, "text", None)
                if piece:
                    text_parts.append(piece)
    prompt = getattr(llm_request, "prompt", None)
    if prompt:
        text_parts.append(prompt)
    return "\n".join(text_parts).lower()


def before_model_guardrails(
    *, callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    text = _extract_text(llm_request)
    if any(pattern in text for pattern in _BLOCK_PATTERNS):
        try:
            callback_context.state["guardrails:blocked"] = True
        except Exception:
            pass
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text=_DEFAULT_BLOCK_MESSAGE)],
            )
        )
    return None
