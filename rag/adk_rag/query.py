from __future__ import annotations

import gc
import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List

from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

from .config import RAGConfig
from .ingest import load_bm25_docs, load_parent_docs


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


def _create_llm(config: RAGConfig, temperature: float | None = None) -> BaseChatModel:
    """Create LLM instance based on provider."""
    temp = temperature if temperature is not None else config.temperature

    if config.llm_provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=config.llm_model, temperature=temp)
    elif config.llm_provider == "ollama":
        from langchain_community.chat_models import ChatOllama

        return ChatOllama(model=config.llm_model, temperature=temp)
    else:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=config.llm_model, temperature=temp)


def _create_rerank_llm(config: RAGConfig) -> BaseChatModel:
    """Create reranking LLM instance based on provider."""
    if config.llm_provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=config.rerank_model, temperature=0)
    elif config.llm_provider == "ollama":
        from langchain_community.chat_models import ChatOllama

        return ChatOllama(model=config.rerank_model, temperature=0)
    else:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=config.rerank_model, temperature=0)


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
        self.embeddings = _create_embeddings(config)
        self.vector_store = self._load_vector_store()
        self.llm = _create_llm(config)

        # Hybrid retrieval components
        self.parent_docs: Dict[str, Document] = {}
        self.bm25_retriever: BM25Retriever | None = None
        self.rerank_llm: BaseChatModel | None = None

        if config.use_hybrid_retrieval:
            self._initialize_hybrid_components()

    def _load_vector_store(self) -> FAISS | None:
        try:
            return FAISS.load_local(
                self.config.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        except Exception:
            return None

    def _initialize_hybrid_components(self) -> None:
        """Initialize BM25 retriever, parent docs, and reranker."""
        # Load parent documents
        self.parent_docs = load_parent_docs(self.config.index_path)

        # Load and build BM25 retriever
        bm25_docs = load_bm25_docs(self.config.index_path)
        if bm25_docs:
            self.bm25_retriever = BM25Retriever.from_documents(bm25_docs)
            self.bm25_retriever.k = self.config.top_k_bm25

        # Initialize reranking LLM if enabled
        if self.config.use_llm_reranking:
            self.rerank_llm = _create_rerank_llm(self.config)

    def _detect_requested_language(self, query: str) -> str:
        """Detect the programming language requested in the query."""
        lang_candidates = ["python", "go", "java", "javascript", "typescript"]
        lower_query = query.lower()

        for lang in lang_candidates:
            if lang in lower_query:
                return lang.capitalize()

        # Default to Python if no language specified
        return "Python"

    def _filter_by_language(
        self, candidates: List[Document], requested_lang: str
    ) -> List[Document]:
        """Filter candidates to match the requested programming language."""
        filtered = []

        for doc in candidates:
            # Extract language tag from chunk content
            lang_match = re.search(r'\[LANG=(\w+)\]', doc.page_content)
            chunk_lang = lang_match.group(1) if lang_match else "Unknown"

            # Include chunks with unknown language for Python (default) to avoid losing recall
            if requested_lang == "Python" and chunk_lang in ("Python", "Unknown"):
                filtered.append(doc)
            elif chunk_lang == requested_lang:
                filtered.append(doc)

        # Use filtered only if enough candidates remain
        min_candidates = max(3, self.config.rerank_top_n)
        if filtered and len(filtered) >= min_candidates:
            return filtered

        # Fallback to original candidates for recall preservation
        return candidates

    def _hybrid_retrieve(self, query: str) -> List[Document]:
        """Perform hybrid retrieval using vector + BM25 ensemble."""
        candidates: List[Document] = []

        # Vector retrieval
        if self.vector_store:
            vector_results = self.vector_store.similarity_search(
                query, k=self.config.top_k_vector
            )
            candidates.extend(vector_results)

        # BM25 retrieval
        if self.bm25_retriever:
            bm25_results = self.bm25_retriever.invoke(query)
            candidates.extend(bm25_results)

        # Deduplicate by content hash
        seen_content = set()
        unique_candidates = []
        for doc in candidates:
            content_hash = hash(doc.page_content)
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_candidates.append(doc)

        return unique_candidates

    def _llm_rerank(self, query: str, docs: List[Document]) -> List[Document]:
        """Rerank candidates using LLM with enhanced prompt for multi-language & completeness."""
        if not docs or not self.rerank_llm:
            return docs[: self.config.rerank_top_n]

        # Detect requested language for emphasis
        requested_lang = self._detect_requested_language(query)

        packed = []
        for i, doc in enumerate(docs):
            snippet = doc.page_content[:1400].replace('\n', ' ').strip()

            # Detect completeness (presence of full API definitions)
            completeness_tag = "[COMPLETE_API]" if re.search(
                r'\b(class|func|def|interface|type|package|func\s+main)\s+\w*',
                snippet, re.I
            ) else "[PARTIAL]"

            # Check if chunk matches requested language
            lang = doc.metadata.get("language", "unknown").lower()
            requested_lang_tag = "[REQUESTED_LANG]" if lang == requested_lang.lower() else ""

            tags = doc.metadata.get("tags", "")
            breadcrumb = doc.metadata.get("breadcrumb", "")

            packed.append(
                f"[{i}] {completeness_tag} {requested_lang_tag} Tags:{tags} Breadcrumb:{breadcrumb}\n{snippet}"
            )

        prompt = (
            "Role: ADK Expert Reranker.\n"
            "Goal: Score each chunk from 0 to 100 for relevance to the query.\n"
            "Prioritize chunks with:\n"
            "- Exact API names matching the query\n"
            "- Complete API definitions over partial snippets\n"
            "- Code examples in the user's requested programming language\n"
            "- Proper handling of multi-language snippets\n"
            f"User Query: {query}\n\n"
            "Chunks:\n" + "\n\n".join(packed) + "\n\n"
            "Return JSON object with 'scores' mapping chunk IDs to numeric scores."
        )

        try:
            response = self.rerank_llm.invoke(prompt)
            match = re.search(r'\{.*\}', response.content, re.DOTALL)

            if not match:
                return docs[: self.config.rerank_top_n]

            scores = json.loads(match.group(0)).get("scores", {})
            ranked_indices = sorted(
                range(len(docs)),
                key=lambda i: float(scores.get(str(i), scores.get(i, 0))),
                reverse=True,
            )
            return [docs[i] for i in ranked_indices[: self.config.rerank_top_n]]

        except Exception as e:
            print(f"Reranking failed: {e}")
            return docs[: self.config.rerank_top_n]

    def _expand_to_parents(
        self, chunks: List[Document], requested_lang: str
    ) -> tuple[List[str], str]:
        """
        Expand retrieved chunks to their parent documents for broader context.

        Returns:
            Tuple of (context_list, formatted_context_block)
        """
        final_contexts: List[str] = []
        seen_parents: set = set()
        context_block = ""

        for chunk in chunks:
            parent_id = chunk.metadata.get("parent_id")

            if parent_id and parent_id in self.parent_docs and parent_id not in seen_parents:
                parent = self.parent_docs[parent_id]

                # Optional: filter parent by language tag
                lang_match = re.search(r'\[LANG=(\w+)\]', parent.page_content)
                parent_lang = lang_match.group(1) if lang_match else "Unknown"

                # Accept unknown language parents for Python queries
                if requested_lang == "Python" and parent_lang not in ("Python", "Unknown"):
                    continue
                elif requested_lang != "Python" and parent_lang not in (requested_lang, "Unknown"):
                    continue

                seen_parents.add(parent_id)
                final_contexts.append(parent.page_content)

                src = os.path.basename(parent.metadata.get("source", "unknown"))
                breadcrumb = parent.metadata.get("breadcrumb", "")

                # XML-style tags for clearer separation
                context_block += (
                    f'<source file="{src}" section="{breadcrumb}">\n'
                    f"{parent.page_content}\n"
                    f"</source>\n\n"
                )

        # If no parents found, fall back to chunks directly
        if not final_contexts:
            for chunk in chunks:
                # Strip the tags prefix for cleaner context
                content = re.sub(r'^\[DOC_\w+\] \[LANG=\w+\] \[\w+\] [^\n]*\n', '', chunk.page_content)
                final_contexts.append(content)
                src = os.path.basename(chunk.metadata.get("source", "unknown"))
                breadcrumb = chunk.metadata.get("breadcrumb", "")
                context_block += (
                    f'<source file="{src}" section="{breadcrumb}">\n'
                    f"{content}\n"
                    f"</source>\n\n"
                )

        return final_contexts, context_block

    def _generate_answer(
        self, query: str, context_block: str, requested_lang: str
    ) -> str:
        """Generate answer using strict grounding prompt."""
        prompt = (
            "You are a technical expert on Google ADK. Answer the user's question "
            "STRICTLY using the provided context. Follow these rules:\n"
            "1. If the answer is not in the context, explicitly state "
            "'I don't know from the provided documentation'.\n"
            "2. When mentioning API classes or methods, use the EXACT names found in the context.\n"
            "3. Use the 'Quote then Explain' pattern: first quote the relevant doc/code, "
            "then provide your explanation.\n"
            f"4. Only provide code or examples in the requested language: {requested_lang}. "
            "If none requested, default to Python but mention other languages exist.\n"
            "5. Clearly indicate the programming language of any code snippet you quote.\n"
            "6. Use XML tags to indicate sources.\n\n"
            f"Context:\n{context_block}\n\n"
            f"Question: {query}\n\n"
            "Answer:"
        )

        response = self.llm.invoke(prompt)
        return response.content

    def query(self, query_text: str) -> Dict[str, Any]:
        """
        Query the RAG system.

        For hybrid mode:
        1. Hybrid retrieval (vector + BM25)
        2. Cross-language filtering
        3. LLM reranking
        4. Parent document expansion
        5. Grounded answer generation

        For legacy mode:
        - Simple vector retrieval + generation
        """
        if not self.vector_store:
            return {
                "answer": "Vector index not found. Run ingestion before querying.",
                "contexts": [],
                "sources": [],
            }

        if self.config.use_hybrid_retrieval:
            return self._query_hybrid(query_text)
        else:
            return self._query_legacy(query_text)

    def _query_hybrid(self, query_text: str) -> Dict[str, Any]:
        """Hybrid retrieval query pipeline."""
        # 1. Detect requested language
        requested_lang = self._detect_requested_language(query_text)

        # 2. Hybrid retrieval
        candidates = self._hybrid_retrieve(query_text)

        if not candidates:
            return {
                "answer": "No relevant documents found.",
                "contexts": [],
                "sources": [],
            }

        # 3. Cross-language filtering
        candidates = self._filter_by_language(candidates, requested_lang)

        # 4. LLM Reranking
        if self.config.use_llm_reranking:
            top_chunks = self._llm_rerank(query_text, candidates)
        else:
            top_chunks = candidates[: self.config.rerank_top_n]

        # 5. Expand to parent documents
        contexts, context_block = self._expand_to_parents(top_chunks, requested_lang)

        # 6. Generate answer
        answer = self._generate_answer(query_text, context_block, requested_lang)

        # Collect sources
        sources = list(
            set(
                os.path.basename(chunk.metadata.get("source", "unknown"))
                for chunk in top_chunks
            )
        )

        gc.collect()

        return RAGResponse(answer, contexts, sources).to_dict()

    def _query_legacy(self, query_text: str) -> Dict[str, Any]:
        """Legacy vector-only query pipeline."""
        try:
            retrieved = self.vector_store.max_marginal_relevance_search(
                query_text, k=self.config.top_k, fetch_k=self.config.fetch_k
            )
        except AttributeError:
            retrieved = self.vector_store.similarity_search(
                query_text, k=self.config.top_k
            )

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
