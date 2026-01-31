from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any, Dict, List, Tuple

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from .chunking import load_documents, load_documents_with_parents
from .config import RAGConfig


def _create_embeddings(config: RAGConfig) -> Embeddings:
    """Create embeddings instance based on provider."""
    if config.llm_provider == "google":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(model=config.embedding_model)
    elif config.llm_provider == "ollama":
        from langchain_community.embeddings import OllamaEmbeddings

        return OllamaEmbeddings(model=config.embedding_model)
    else:
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model=config.embedding_model)


def ingest_documents(config: RAGConfig) -> List[Document]:
    """Legacy ingestion function - returns only chunks."""
    return load_documents(config.docs_path, config.chunk_size, config.chunk_overlap)


def ingest_documents_with_parents(
    config: RAGConfig,
) -> Tuple[List[Document], Dict[str, Document]]:
    """
    Ingest documents with parent-child hierarchy.

    Returns:
        Tuple of (child_chunks, parent_docs)
    """
    return load_documents_with_parents(
        config.docs_path, config.chunk_size, config.chunk_overlap
    )


def build_vector_store(config: RAGConfig, documents: List[Document]) -> FAISS:
    """Build a FAISS vector store from documents."""
    embeddings = _create_embeddings(config)
    return FAISS.from_documents(documents, embeddings)


def save_vector_store(store: FAISS, index_path: str) -> None:
    """Save FAISS vector store to disk."""
    Path(index_path).mkdir(parents=True, exist_ok=True)
    store.save_local(index_path)


def save_parent_docs(parent_docs: Dict[str, Document], index_path: str) -> None:
    """
    Save parent documents to disk for later retrieval.

    Stores as pickle for full Document object preservation.
    """
    path = Path(index_path)
    path.mkdir(parents=True, exist_ok=True)

    # Save as pickle for full fidelity
    pickle_path = path / "parent_docs.pkl"
    with open(pickle_path, "wb") as f:
        pickle.dump(parent_docs, f)

    # Also save a JSON index for debugging/inspection
    json_path = path / "parent_docs_index.json"
    index_data = {
        pid: {
            "source": doc.metadata.get("source", ""),
            "breadcrumb": doc.metadata.get("breadcrumb", ""),
            "tags": doc.metadata.get("tags", ""),
            "content_preview": doc.page_content[:200] + "..."
            if len(doc.page_content) > 200
            else doc.page_content,
        }
        for pid, doc in parent_docs.items()
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2)


def load_parent_docs(index_path: str) -> Dict[str, Document]:
    """Load parent documents from disk."""
    pickle_path = Path(index_path) / "parent_docs.pkl"
    if not pickle_path.exists():
        return {}

    with open(pickle_path, "rb") as f:
        return pickle.load(f)


def save_bm25_data(documents: List[Document], index_path: str) -> None:
    """
    Save document data needed to reconstruct BM25 retriever.

    BM25Retriever cannot be pickled directly, so we store the
    document contents and metadata to reconstruct it at query time.
    """
    path = Path(index_path)
    path.mkdir(parents=True, exist_ok=True)

    bm25_path = path / "bm25_docs.pkl"
    # Store serializable representation
    docs_data = [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in documents
    ]
    with open(bm25_path, "wb") as f:
        pickle.dump(docs_data, f)


def load_bm25_docs(index_path: str) -> List[Document]:
    """Load documents for BM25 reconstruction."""
    bm25_path = Path(index_path) / "bm25_docs.pkl"
    if not bm25_path.exists():
        return []

    with open(bm25_path, "rb") as f:
        docs_data = pickle.load(f)

    return [
        Document(page_content=d["page_content"], metadata=d["metadata"])
        for d in docs_data
    ]


def save_ingestion_metadata(
    config: RAGConfig, chunk_count: int, parent_count: int, index_path: str
) -> None:
    """Save metadata about the ingestion for debugging and version tracking."""
    path = Path(index_path)
    path.mkdir(parents=True, exist_ok=True)

    metadata = {
        "chunk_count": chunk_count,
        "parent_count": parent_count,
        "chunk_size": config.chunk_size,
        "chunk_overlap": config.chunk_overlap,
        "embedding_model": config.embedding_model,
        "use_hybrid_retrieval": config.use_hybrid_retrieval,
        "docs_path": config.docs_path,
    }

    meta_path = path / "ingestion_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def run_ingestion(config: RAGConfig) -> int:
    """
    Run the full ingestion pipeline.

    For hybrid retrieval (default), creates:
    - FAISS vector index
    - Parent documents pickle
    - BM25 document data

    Returns:
        Number of chunks ingested.
    """
    if config.use_hybrid_retrieval:
        # Use new parent-child chunking
        documents, parent_docs = ingest_documents_with_parents(config)

        if not documents:
            return 0

        # Build and save vector store
        store = build_vector_store(config, documents)
        save_vector_store(store, config.index_path)

        # Save parent documents for context expansion
        save_parent_docs(parent_docs, config.index_path)

        # Save BM25 data for hybrid retrieval
        save_bm25_data(documents, config.index_path)

        # Save metadata
        save_ingestion_metadata(
            config, len(documents), len(parent_docs), config.index_path
        )

        print(f"Saved {len(parent_docs)} parent documents")
        print(f"Saved BM25 data for {len(documents)} chunks")

        return len(documents)
    else:
        # Legacy mode: simple chunking, vector-only retrieval
        documents = ingest_documents(config)
        if not documents:
            return 0
        store = build_vector_store(config, documents)
        save_vector_store(store, config.index_path)
        return len(documents)
