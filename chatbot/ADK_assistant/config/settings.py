from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union


@dataclass(frozen=True)
class Settings:
    app_name: str = "adk_chatbot"
    rag_mcp_url: str = "http://localhost:8000/sse"
    base_dir: str = "."
    llm_model: Union[str, object] = "gemini-2.0-flash"
    max_rag_iterations: int = 3
    max_refine_iterations: int = 2
    allowed_shell_commands: List[str] = None

    @staticmethod
    def _default_allowlist() -> List[str]:
        return [
            "ls",
            "rg",
            "cat",
            "python",
            "python3",
            "pytest",
        ]


def _resolve_llm_model(provider: str, model_name: str) -> Union[str, object]:
    if provider.lower() == "openai":
        from google.adk.models.lite_llm import LiteLlm

        if "/" in model_name:
            return LiteLlm(model=model_name)
        return LiteLlm(model=f"openai/{model_name}")
    return model_name


def get_settings() -> Settings:
    base_dir = os.getenv("CHATBOT_BASE_DIR", str(Path(__file__).resolve().parents[2]))
    rag_mcp_url = os.getenv("RAG_MCP_URL", "http://localhost:8000/sse")
    llm_provider = os.getenv("ADK_LLM_PROVIDER", "openai")
    llm_model_name = os.getenv("ADK_LLM_MODEL", "gpt-4.1-mini")
    llm_model = _resolve_llm_model(llm_provider, llm_model_name)
    max_rag_iterations = int(os.getenv("RAG_MAX_ITERS", "3"))
    max_refine_iterations = int(os.getenv("REFINE_MAX_ITERS", "2"))
    allowlist = os.getenv("SHELL_ALLOWLIST", "")
    allowed_shell_commands = (
        [cmd.strip() for cmd in allowlist.split(",") if cmd.strip()]
        if allowlist
        else Settings._default_allowlist()
    )
    return Settings(
        app_name=os.getenv("ADK_APP_NAME", "adk_chatbot"),
        rag_mcp_url=rag_mcp_url,
        base_dir=base_dir,
        llm_model=llm_model,
        max_rag_iterations=max_rag_iterations,
        max_refine_iterations=max_refine_iterations,
        allowed_shell_commands=allowed_shell_commands,
    )
