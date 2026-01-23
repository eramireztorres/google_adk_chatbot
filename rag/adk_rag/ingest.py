from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from .chunking import load_documents
from .config import RAGConfig


def ingest_documents(config: RAGConfig) -> List[Document]:
    return load_documents(config.docs_path, config.chunk_size, config.chunk_overlap)


def build_vector_store(config: RAGConfig, documents: List[Document]) -> FAISS:
    embeddings = OpenAIEmbeddings(model=config.embedding_model)
    return FAISS.from_documents(documents, embeddings)


def save_vector_store(store: FAISS, index_path: str) -> None:
    Path(index_path).mkdir(parents=True, exist_ok=True)
    store.save_local(index_path)


def run_ingestion(config: RAGConfig) -> int:
    documents = ingest_documents(config)
    if not documents:
        return 0
    store = build_vector_store(config, documents)
    save_vector_store(store, config.index_path)
    return len(documents)
