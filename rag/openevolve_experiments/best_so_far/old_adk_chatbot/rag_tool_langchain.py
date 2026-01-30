from typing import Dict, Any, List
import lancedb
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.adk_chatbot.knowledge_base_langchain import (
    DEFAULT_LC_DB_PATH,
    DEFAULT_LC_TABLE_NAME,
    get_langchain_vector_store,
)


class RAGSystemLangchain:
    def __init__(self) -> None:
        self.vector_store = get_langchain_vector_store()
        self.llm = ChatOpenAI(model="gpt-4.1-mini")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self._preferred_code_sources = [
            "adk-docs-tools-custom.md",
            "adk-docs-tools-custom-function-tools.md",
            "adk-docs-agents-multi-agents.md",
        ]

    def _call_llm_text(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content

    def _rewrite_query(self, query_str: str) -> str:
        prompt = (
            "Rewrite the user query as a standalone search query for Google ADK docs. "
            "If it is already standalone, return it unchanged. Return only the query.\n\n"
            f"USER QUERY:\n{query_str}\n"
        )
        rewritten = self._call_llm_text(prompt).strip()
        return rewritten or query_str

    def _augment_query(self, query_str: str) -> str:
        lowered = query_str.lower()
        if any(token in lowered for token in ("example", "code", "snippet")):
            return f"{query_str} example code"
        return query_str

    def _expand_queries(self, query_str: str) -> List[str]:
        prompt = (
            "Generate 3 to 5 alternative search queries for the ADK docs. "
            "Focus on synonyms and likely doc headings. Return one per line.\n\n"
            f"QUERY:\n{query_str}\n"
        )
        raw = self._call_llm_text(prompt)
        lines = [line.strip("- ").strip() for line in raw.splitlines() if line.strip()]
        uniq = []
        for line in lines:
            if line and line not in uniq:
                uniq.append(line)
        return uniq[:5] if uniq else [query_str]

    def _hyde_query(self, query_str: str) -> str:
        prompt = (
            "Write a short hypothetical answer (3-5 sentences) to the query, "
            "as if it were answered from ADK docs. Do not include code. "
            "Return only the hypothetical answer.\n\n"
            f"QUERY:\n{query_str}\n"
        )
        return self._call_llm_text(prompt).strip()

    def _rrf_fuse(self, ranked_lists: List[List[Any]], k: int = 60) -> List[Any]:
        scores: Dict[str, float] = {}
        doc_map: Dict[str, Any] = {}
        for docs in ranked_lists:
            for rank, doc in enumerate(docs):
                key = doc.page_content
                scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank + 1)
                if key not in doc_map:
                    doc_map[key] = doc
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return [doc_map[key] for key, _ in ranked]

    def _has_code(self, text: str) -> bool:
        lowered = text.lower()
        return "```" in text or "\n    " in text or "def " in lowered or "class " in lowered

    def _is_navigation_chunk(self, text: str) -> bool:
        lowered = text.lower()
        return (
            "table of contents" in lowered
            or "permanent link" in lowered
            or "supported in adk" in lowered
        )

    def _retrieve_fusion(self, query_str: str, k: int = 8) -> List[Any]:
        rewritten = self._rewrite_query(query_str)
        augmented = self._augment_query(rewritten)
        expanded = self._expand_queries(augmented)
        hyde = self._hyde_query(augmented)

        queries = [augmented] + [q for q in expanded if q != augmented]
        if hyde:
            queries.append(hyde)

        ranked_lists: List[List[Any]] = []
        for q in queries:
            ranked_lists.append(self.vector_store.similarity_search(q, k=k))

        fused = self._rrf_fuse(ranked_lists)
        return fused[:k]

    def _boost_by_source(self, docs: List[Any]) -> List[Any]:
        preferred = []
        others = []
        for doc in docs:
            source = (doc.metadata or {}).get("source", "")
            if any(name in source for name in self._preferred_code_sources):
                preferred.append(doc)
            else:
                others.append(doc)
        return preferred + others

    def _retrieve_code_chunks(self, query_str: str, k: int = 12) -> List[Document]:
        conn = lancedb.connect(DEFAULT_LC_DB_PATH)
        table = conn.open_table(DEFAULT_LC_TABLE_NAME)
        embedding = self.embeddings.embed_query(query_str)
        rows = table.search(embedding).limit(k * 4).to_list()
        docs = []
        keyword = None
        lowered_query = query_str.lower()
        if "functiontool" in lowered_query:
            keyword = "functiontool"
        for row in rows:
            metadata = row.get("metadata") or {}
            if metadata.get("type") != "code":
                continue
            content = row.get("text") or row.get("page_content") or ""
            if not content:
                continue
            lowered_content = content.lower()
            if keyword and keyword not in lowered_content:
                continue
            docs.append(Document(page_content=content, metadata=metadata))
        return docs[:k]

    def query(self, query_str: str) -> Dict[str, Any]:
        retrieved = self._retrieve_fusion(query_str, k=12)
        code_query = any(token in query_str.lower() for token in ("example", "code", "snippet"))
        if code_query:
            code_chunks = self._retrieve_code_chunks(query_str, k=12)
            if code_chunks:
                retrieved = code_chunks + retrieved
            filtered = [d for d in retrieved if not self._is_navigation_chunk(d.page_content)]
            if filtered:
                retrieved = filtered
            retrieved = self._boost_by_source(retrieved)
        if code_query and retrieved and not any(self._has_code(d.page_content) for d in retrieved):
            fallback_query = f"{query_str} FunctionTool example"
            retrieved = self.vector_store.similarity_search(fallback_query, k=20)
            retrieved = self._boost_by_source(retrieved)
        context = "\n\n".join(d.page_content for d in retrieved)
        prompt = (
            "You are a helpful assistant answering strictly from the provided context.\n"
            "If the answer or code is not explicitly present in the context, say\n"
            "\"Not found in the provided documentation.\" Do not guess imports or APIs.\n\n"
            f"CONTEXT:\n{context}\n\nQUESTION:\n{query_str}\n"
        )
        answer = self.llm.invoke(prompt).content
        contexts = [d.page_content for d in retrieved]
        return {"answer": answer, "contexts": contexts}


_rag_system_langchain_cache: RAGSystemLangchain | None = None


def evaluate_rag_langchain(docs_path: str, query: str) -> Dict[str, Any]:
    global _rag_system_langchain_cache
    try:
        if _rag_system_langchain_cache is None:
            _rag_system_langchain_cache = RAGSystemLangchain()

        query = query.strip()
        if not query:
            return {"answer": "Error: Empty query.", "contexts": []}

        return _rag_system_langchain_cache.query(query)
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "contexts": []}
