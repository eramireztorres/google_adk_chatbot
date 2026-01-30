import os
from typing import Optional

from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

DEFAULT_LLAMAINDEX_DIR = "/home/erick/repo/adk_chatbot/data/llamaindex_storage"
DEFAULT_LLAMAINDEX_MODEL = "gpt-4.1-mini"
DEFAULT_LLAMAINDEX_EMBED_MODEL = "text-embedding-3-small"


def configure_llamaindex_settings(
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
    model: Optional[str] = None,
    embed_model: Optional[str] = None,
) -> None:
    """Configure LlamaIndex Settings for embeddings, LLM, and chunking."""
    llm_model = model or os.getenv("LLAMAINDEX_LLM", DEFAULT_LLAMAINDEX_MODEL)
    embed = embed_model or os.getenv("LLAMAINDEX_EMBED_MODEL", DEFAULT_LLAMAINDEX_EMBED_MODEL)

    Settings.llm = OpenAI(model=llm_model)
    Settings.embed_model = OpenAIEmbedding(model=embed)

    size = chunk_size or int(os.getenv("LLAMAINDEX_CHUNK_SIZE", "1024"))
    overlap = chunk_overlap if chunk_overlap is not None else int(os.getenv("LLAMAINDEX_CHUNK_OVERLAP", "128"))
    Settings.node_parser = SentenceSplitter(chunk_size=size, chunk_overlap=overlap)


def load_llamaindex_index(persist_dir: str = DEFAULT_LLAMAINDEX_DIR):
    """Load a persisted LlamaIndex index from disk."""
    configure_llamaindex_settings()

    if not os.path.isdir(persist_dir):
        raise FileNotFoundError(
            f"LlamaIndex storage not found at {persist_dir}. Run run_ingestion_llamaindex.py first."
        )

    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    return load_index_from_storage(storage_context)
