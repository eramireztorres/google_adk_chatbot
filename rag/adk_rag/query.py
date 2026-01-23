from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from .config import RAGConfig


@dataclass
class RAGResponse:
    answer: str
    contexts: List[str]
    sources: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "answer": self.answer,
            "contexts": self.contexts,
            "sources": self.sources,
        }


class RAGSystem:
    def __init__(self, config: RAGConfig):
        self.config = config
        self.embeddings = OpenAIEmbeddings(model=config.embedding_model)
        self.vector_store = self._load_vector_store()
        self.llm = ChatOpenAI(model=config.llm_model, temperature=config.temperature)

    def _load_vector_store(self) -> FAISS | None:
        try:
            return FAISS.load_local(
                self.config.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        except Exception:
            return None

    def query(self, query_text: str) -> Dict[str, Any]:
        if not self.vector_store:
            return {
                "answer": "Vector index not found. Run ingestion before querying.",
                "contexts": [],
                "sources": [],
            }

        try:
            retrieved = self.vector_store.max_marginal_relevance_search(
                query_text, k=self.config.top_k, fetch_k=self.config.fetch_k
            )
        except AttributeError:
            retrieved = self.vector_store.similarity_search(query_text, k=self.config.top_k)

        contexts = [doc.page_content for doc in retrieved]
        sources = [doc.metadata.get("source", "unknown") for doc in retrieved]
        context_block = ""
        for idx, (content, source) in enumerate(zip(contexts, sources), start=1):
            context_block += f"Source {idx} ({source}):\n{content}\n\n"

        prompt = (
            "You are an expert assistant for Google ADK documentation.\n"
            f"Question: {query_text}\n\n"
            f"Context:\n{context_block}\n\n"
            "Answer the question based strictly on the context provided. "
            "If the context contains code examples, use them to illustrate your answer. "
            "Be concise, accurate, and faithful to the context. "
            "If you cannot answer from the context, say 'I don't know based on the provided context.'"
        )

        response = self.llm.invoke(prompt)
        return RAGResponse(response.content, contexts, sources).to_dict()
