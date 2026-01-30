from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

import yaml


# Default models per provider
PROVIDER_DEFAULTS = {
    "google": {
        "llm_model": "gemini-2.5-flash-lite",
        "embedding_model": "models/text-embedding-004",
        "rerank_model": "gemini-2.5-flash-lite",
    },
    "openai": {
        "llm_model": "gpt-4.1-mini",
        "embedding_model": "text-embedding-3-large",
        "rerank_model": "gpt-4.1-mini",
    },
}


def _detect_provider() -> str:
    """
    Auto-detect LLM provider based on available API keys.

    Priority:
    1. Explicit RAG_LLM_PROVIDER env var
    2. If OPENAI_API_KEY is set -> openai
    3. If GOOGLE_API_KEY is set -> google
    4. Default to google (requires GOOGLE_API_KEY at runtime)
    """
    explicit = os.getenv("RAG_LLM_PROVIDER", "").strip().lower()
    if explicit in ("google", "openai"):
        return explicit

    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GOOGLE_API_KEY"):
        return "google"

    # Default to google - will fail at runtime if GOOGLE_API_KEY not set
    return "google"


@dataclass
class RAGConfig:
    docs_path: str = "../docs/adk_docs"
    index_path: str = "./index"
    chunk_size: int = 500
    chunk_overlap: int = 100

    # Hybrid retrieval settings
    top_k_vector: int = 20
    top_k_bm25: int = 20
    weight_vector: float = 0.5
    weight_bm25: float = 0.5
    use_hybrid_retrieval: bool = True

    # Reranking settings
    rerank_top_n: int = 8
    use_llm_reranking: bool = True

    # Legacy settings (kept for backward compatibility)
    top_k: int = 8
    fetch_k: int = 10

    # Provider settings
    llm_provider: str = field(default_factory=_detect_provider)

    # Model settings (defaults set based on provider in load_config)
    embedding_model: str = ""
    llm_model: str = ""
    rerank_model: str = ""
    temperature: float = 0.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RAGConfig":
        cfg = cls()
        for key, value in data.items():
            if hasattr(cfg, key):
                setattr(cfg, key, value)
        return cfg


def _resolve_path(value: str, base_dir: Path) -> str:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    return str(path)


def load_config(config_path: str | None = None) -> RAGConfig:
    if config_path:
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
    else:
        path = Path(__file__).with_name("config.yaml")

    data: Dict[str, Any] = {}
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            loaded = yaml.safe_load(handle) or {}
            if isinstance(loaded, dict):
                data = loaded

    cfg = RAGConfig.from_dict(data)
    base_dir = path.parent
    cfg.docs_path = _resolve_path(cfg.docs_path, base_dir)
    cfg.index_path = _resolve_path(cfg.index_path, base_dir)

    # Re-detect provider (may have changed since dataclass init)
    cfg.llm_provider = _detect_provider()

    # Apply provider-specific defaults for empty model fields
    provider_defaults = PROVIDER_DEFAULTS.get(cfg.llm_provider, PROVIDER_DEFAULTS["google"])

    if not cfg.embedding_model:
        cfg.embedding_model = provider_defaults["embedding_model"]
    if not cfg.llm_model:
        cfg.llm_model = provider_defaults["llm_model"]
    if not cfg.rerank_model:
        cfg.rerank_model = provider_defaults["rerank_model"]

    # Environment variable overrides (provider-agnostic)
    if os.getenv("RAG_EMBEDDING_MODEL"):
        cfg.embedding_model = os.getenv("RAG_EMBEDDING_MODEL")
    if os.getenv("RAG_LLM_MODEL"):
        cfg.llm_model = os.getenv("RAG_LLM_MODEL")
    if os.getenv("RAG_RERANK_MODEL"):
        cfg.rerank_model = os.getenv("RAG_RERANK_MODEL")

    # Legacy OpenAI env vars (for backward compatibility)
    if os.getenv("OPENAI_EMBEDDING_MODEL") and cfg.llm_provider == "openai":
        cfg.embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL")
    if os.getenv("OPENAI_LLM_MODEL") and cfg.llm_provider == "openai":
        cfg.llm_model = os.getenv("OPENAI_LLM_MODEL")

    # Temperature override
    temp_env = os.getenv("RAG_TEMPERATURE") or os.getenv("OPENAI_TEMPERATURE")
    if temp_env:
        try:
            cfg.temperature = float(temp_env)
        except ValueError:
            pass

    # Hybrid retrieval env overrides
    if "RAG_USE_HYBRID" in os.environ:
        cfg.use_hybrid_retrieval = os.environ["RAG_USE_HYBRID"].lower() in ("true", "1", "yes")
    if "RAG_USE_RERANKING" in os.environ:
        cfg.use_llm_reranking = os.environ["RAG_USE_RERANKING"].lower() in ("true", "1", "yes")

    return cfg
