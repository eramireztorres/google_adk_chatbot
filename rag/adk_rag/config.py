from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml
import os


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

    # Model settings
    embedding_model: str = "text-embedding-3-large"
    llm_model: str = "gpt-4.1-mini"
    rerank_model: str = "gpt-4.1-mini"
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
    cfg.embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", cfg.embedding_model)
    cfg.llm_model = os.getenv("OPENAI_LLM_MODEL", cfg.llm_model)
    cfg.rerank_model = os.getenv("OPENAI_RERANK_MODEL", cfg.rerank_model)

    if "OPENAI_TEMPERATURE" in os.environ:
        try:
            cfg.temperature = float(os.environ["OPENAI_TEMPERATURE"])
        except ValueError:
            pass

    # Hybrid retrieval env overrides
    if "RAG_USE_HYBRID" in os.environ:
        cfg.use_hybrid_retrieval = os.environ["RAG_USE_HYBRID"].lower() in ("true", "1", "yes")
    if "RAG_USE_RERANKING" in os.environ:
        cfg.use_llm_reranking = os.environ["RAG_USE_RERANKING"].lower() in ("true", "1", "yes")

    return cfg
