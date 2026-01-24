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

_ADK_KEYWORDS = [
    "adk",
    "agent development kit",
    "agent",
    "llm agent",
    "workflow agent",
    "custom agent",
    "multi-agent",
    "agenttool",
    "agent tool",
    "agentconfig",
    "agent config",
    "llmagent",
    "functiontool",
    "function tool",
    "toolcontext",
    "tool context",
    "toolset",
    "mcp",
    "model context protocol",
    "mcp tool",
    "mcp toolset",
    "a2a",
    "agent-to-agent",
    "openapi",
    "openapi tools",
    "built-in tools",
    "tool confirmation",
    "tool performance",
    "gemini",
    "vertex",
    "vertex ai",
    "lite llm",
    "litellm",
    "model",
    "provider",
    "authentication",
    "api key",
    "runtime",
    "runconfig",
    "resume",
    "session",
    "sessions",
    "state",
    "events",
    "streaming",
    "sse",
    "websocket",
    "bidi streaming",
    "run_live",
    "cloud run",
    "gke",
    "agent engine",
    "deploy",
    "logging",
    "trace",
    "observability",
    "agentops",
    "arize",
    "phoenix",
    "weave",
    "eval",
    "evaluation",
    "adk web",
    "visual builder",
    "apps",
    "cli",
    "api reference",
    "safety",
    "context",
    "context caching",
    "context compaction",
]

_PROJECT_MARKERS = [
    "create project",
    "new project",
    "project scaffold",
    "scaffold",
    "generate project",
    "initialize project",
    "project setup",
    "write files",
    "create files",
    "generate files",
    "file structure",
    "folder structure",
    "repo",
    "repository",
    "codebase",
]


def _extract_user_text(callback_context: CallbackContext) -> str:
    user_content = getattr(callback_context, "user_content", None)
    if user_content is None:
        return ""
    parts = getattr(user_content, "parts", None) or []
    text_parts = []
    for part in parts:
        piece = getattr(part, "text", None)
        if piece:
            text_parts.append(piece)
    return "\n".join(text_parts).lower()


def _looks_like_adk_question(text: str) -> bool:
    return any(keyword in text for keyword in _ADK_KEYWORDS)


def _looks_like_project_request(text: str) -> bool:
    return any(marker in text for marker in _PROJECT_MARKERS)


def _is_prompt_injection(text: str) -> bool:
    return any(pattern in text for pattern in _BLOCK_PATTERNS)


def before_agent_routing_guardrails(
    *, callback_context: CallbackContext
) -> Optional[types.Content]:
    text = _extract_user_text(callback_context)
    if not text:
        return None

    if _is_prompt_injection(text):
        try:
            callback_context.state["guardrails:blocked"] = True
        except Exception:
            pass
        return types.Content(role="model", parts=[types.Part(text=_DEFAULT_BLOCK_MESSAGE)])

    is_adk = _looks_like_adk_question(text)
    is_project = _looks_like_project_request(text)

    if is_adk and not is_project:
        callback_context.state["routing:force_rag"] = True
    if is_project:
        callback_context.state["routing:force_rag"] = False
    return None


def before_model_routing_guardrails(
    *, callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    text = _extract_user_text(callback_context)
    if _is_prompt_injection(text):
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
