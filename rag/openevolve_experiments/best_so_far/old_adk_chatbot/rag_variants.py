import os
import hashlib
from typing import Dict, Any, List, Tuple

from agno.agent import Agent
from agno.filters import AND, EQ, GT
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reranker.cohere import CohereReranker
from agno.models.openai import OpenAIChat
from agno.vectordb.lancedb import LanceDb, SearchType

DEFAULT_DB_PATH = "/home/erick/repo/adk_chatbot/data/lancedb"

try:
    from agno.knowledge.reranker.sentence_transformer import SentenceTransformerReranker
except Exception:
    SentenceTransformerReranker = None

try:
    from agno.knowledge.reranker.infinity import InfinityReranker
except Exception:
    InfinityReranker = None


class BaseRagVariant:
    name = "base"

    def query(self, query_str: str) -> Dict[str, Any]:
        raise NotImplementedError

    @staticmethod
    def _is_code_query(query_str: str) -> bool:
        lowered = query_str.lower()
        return any(token in lowered for token in ("code", "example", "snippet", "import", "python", "usage"))

    @staticmethod
    def _contexts_have_code(contexts: List[str]) -> bool:
        for ctx in contexts:
            if "```" in ctx:
                return True
            if "from google.adk" in ctx or "import google.adk" in ctx:
                return True
        return False

    @staticmethod
    def _extract_code_blocks(contexts: List[str]) -> List[str]:
        blocks: List[str] = []
        for ctx in contexts:
            if "```" not in ctx:
                continue
            parts = ctx.split("```")
            for idx in range(1, len(parts), 2):
                block = parts[idx].strip()
                if block:
                    blocks.append(block)
        return blocks

    @classmethod
    def _code_filters(cls) -> List[Any]:
        return [AND(EQ("content_kind", "code"), GT("code_density", 0.35))]

    @staticmethod
    def _language_filter(query_str: str) -> str | None:
        lowered = query_str.lower()
        if "python" in lowered:
            return "python"
        if "java" in lowered:
            return "java"
        if "go" in lowered or "golang" in lowered:
            return "go"
        return None


def _build_reranker():
    reranker_pref = os.getenv("RAG_RERANKER", "").strip().lower()
    if reranker_pref == "cohere":
        if os.getenv("COHERE_API_KEY"):
            return CohereReranker(model="rerank-v3.5")
        return None
    if reranker_pref == "sentence_transformer":
        if SentenceTransformerReranker is not None:
            return SentenceTransformerReranker()
        return None
    if reranker_pref == "infinity":
        if InfinityReranker is not None:
            return InfinityReranker(
                url=os.getenv("INFINITY_URL"),
                host=os.getenv("INFINITY_HOST", "localhost"),
                port=int(os.getenv("INFINITY_PORT", "7997")),
                api_key=os.getenv("INFINITY_API_KEY"),
            )
        return None
    if reranker_pref == "none":
        return None
    if os.getenv("COHERE_API_KEY"):
        return CohereReranker(model="rerank-v3.5")
    return None


class AgnoRerankRag(BaseRagVariant):
    name = "agno_rerank"

    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path
        self.agent = None
        self.knowledge = None
        self._initialize_system()

    def _initialize_system(self) -> None:
        reranker = _build_reranker()

        try:
            import tantivy  # noqa: F401
            search_type = SearchType.hybrid
        except Exception:
            search_type = SearchType.vector

        self.knowledge = Knowledge(
            vector_db=LanceDb(
                table_name="adk_docs",
                uri=self.db_path,
                search_type=search_type,
                embedder=OpenAIEmbedder(id="text-embedding-3-small"),
                reranker=reranker,
            ),
        )

        self.agent = Agent(
            model=OpenAIChat(id="gpt-4.1-mini"),
            instructions=(
                "Answer only using the retrieved documentation context. "
                "Do not guess imports or APIs."
            ),
            knowledge=self.knowledge,
            search_knowledge=True,
            markdown=False,
        )

    def query(self, query_str: str) -> Dict[str, Any]:
        knowledge_filters = None
        if self._is_code_query(query_str):
            knowledge_filters = self._code_filters()
            lang_filter = self._language_filter(query_str)
            if lang_filter:
                knowledge_filters = [
                    AND(
                        EQ("content_kind", "code"),
                        GT("code_density", 0.35),
                        EQ("code_lang", lang_filter),
                    )
                ]
        response_obj = self.agent.run(query_str, knowledge_filters=knowledge_filters)
        answer = response_obj.content

        contexts = []
        if hasattr(response_obj, "sources") and response_obj.sources:
            contexts = [
                source.content for source in response_obj.sources if hasattr(source, "content")
            ]
        else:
            try:
                manual_results = self.knowledge.search(
                    query=query_str,
                    filters=knowledge_filters,
                )
                if manual_results:
                    contexts = [res.content for res in manual_results]
            except Exception:
                pass

        if os.getenv("RAG_LOG_CONTEXTS") == "1":
            print(f"[RAG] Query: {query_str}")
            for idx, ctx in enumerate(contexts[:5], start=1):
                preview = ctx.replace("\n", " ")[:160]
                print(f"[RAG] Context {idx}: len={len(ctx)} preview={preview}")

        if not contexts:
            return {"answer": "Not found in the provided documentation.", "contexts": contexts}

        if self._is_code_query(query_str):
            code_blocks = self._extract_code_blocks(contexts)
            if not code_blocks:
                return {"answer": "Not found in the provided documentation.", "contexts": contexts}
            answer = "```python\n" + "\n\n".join(code_blocks) + "\n```"
            return {"answer": answer, "contexts": contexts}

        return {"answer": answer, "contexts": contexts}


class FusionRag(BaseRagVariant):
    name = "fusion_rrf"

    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path
        self.knowledge = None
        self.answer_agent = None
        self.rewrite_agent = None
        self._initialize_system()

    def _initialize_system(self) -> None:
        reranker = _build_reranker()

        try:
            import tantivy  # noqa: F401
            search_type = SearchType.hybrid
        except Exception:
            search_type = SearchType.vector

        self.knowledge = Knowledge(
            vector_db=LanceDb(
                table_name="adk_docs",
                uri=self.db_path,
                search_type=search_type,
                embedder=OpenAIEmbedder(id="text-embedding-3-small"),
                reranker=reranker,
            ),
        )

        self.answer_agent = Agent(
            model=OpenAIChat(id="gpt-4.1-mini"),
            instructions=(
                "Answer using only the provided context. "
                "If the answer is not explicitly present, say "
                "\"Not found in the provided documentation.\" "
                "Do not guess imports or APIs."
            ),
            markdown=False,
        )

        self.rewrite_agent = Agent(
            model=OpenAIChat(id="gpt-4.1-mini"),
            instructions=(
                "Generate concise search query rewrites for the given question. "
                "Return one query per line, no numbering, no extra text. "
                "Keep them short and concrete."
            ),
            markdown=False,
        )

    def _generate_queries(self, query_str: str) -> List[str]:
        desired = max(1, int(os.getenv("RAG_FUSION_QUERIES", "4")))
        try:
            raw = self.rewrite_agent.run(
                f"Question: {query_str}\nGenerate {desired} rewrites."
            ).content
            candidates = [line.strip() for line in raw.splitlines() if line.strip()]
        except Exception:
            candidates = []

        combined = [query_str] + candidates
        seen = set()
        queries = []
        for q in combined:
            if q.lower() in seen:
                continue
            seen.add(q.lower())
            queries.append(q)
        return queries[: max(1, desired + 1)]

    def _doc_key(self, doc: Any) -> Tuple[str, str]:
        source = ""
        if hasattr(doc, "metadata") and isinstance(doc.metadata, dict):
            source = str(doc.metadata.get("source") or doc.metadata.get("path") or "")
        content = doc.content if hasattr(doc, "content") else ""
        digest = hashlib.sha1(content.encode("utf-8")).hexdigest()
        return (source, digest)

    def _rrf_fuse(self, results_by_query: List[List[Any]], rrf_k: int) -> List[Any]:
        scores: Dict[Tuple[str, str], Tuple[Any, float]] = {}
        for results in results_by_query:
            for rank, doc in enumerate(results):
                key = self._doc_key(doc)
                score = 1.0 / (rrf_k + rank + 1)
                if key in scores:
                    scores[key] = (scores[key][0], scores[key][1] + score)
                else:
                    scores[key] = (doc, score)
        ranked = sorted(scores.values(), key=lambda item: item[1], reverse=True)
        return [doc for doc, _score in ranked]

    def query(self, query_str: str) -> Dict[str, Any]:
        top_k = int(os.getenv("RAG_FUSION_TOP_K", "10"))
        max_ctx = int(os.getenv("RAG_FUSION_TOP_N", "8"))
        rrf_k = int(os.getenv("RAG_FUSION_RRF_K", "60"))

        knowledge_filters = None
        if self._is_code_query(query_str):
            knowledge_filters = self._code_filters()
            lang_filter = self._language_filter(query_str)
            if lang_filter:
                knowledge_filters = [
                    AND(
                        EQ("content_kind", "code"),
                        GT("code_density", 0.35),
                        EQ("code_lang", lang_filter),
                    )
                ]
        queries = self._generate_queries(query_str)
        results_by_query = []
        for q in queries:
            results = self.knowledge.search(
                query=q,
                max_results=top_k,
                filters=knowledge_filters,
            )
            results_by_query.append(results or [])

        fused = self._rrf_fuse(results_by_query, rrf_k=rrf_k)
        contexts = [doc.content for doc in fused[:max_ctx] if hasattr(doc, "content")]

        if os.getenv("RAG_LOG_CONTEXTS") == "1":
            print(f"[RAG] Fusion queries ({len(queries)}): {queries}")
            for idx, ctx in enumerate(contexts[:5], start=1):
                preview = ctx.replace("\n", " ")[:160]
                print(f"[RAG] Context {idx}: len={len(ctx)} preview={preview}")

        if not contexts:
            return {"answer": "Not found in the provided documentation.", "contexts": []}
        if self._is_code_query(query_str):
            code_blocks = self._extract_code_blocks(contexts)
            if not code_blocks:
                return {"answer": "Not found in the provided documentation.", "contexts": contexts}
            answer = "```python\n" + "\n\n".join(code_blocks) + "\n```"
            return {"answer": answer, "contexts": contexts}

        context_block = "\n\n".join(contexts)
        prompt = (
            "Use only the context below to answer the question.\n\n"
            f"Context:\n{context_block}\n\nQuestion: {query_str}"
        )
        response_obj = self.answer_agent.run(prompt)
        answer = response_obj.content

        return {"answer": answer, "contexts": contexts}


class LlamaIndexRag(BaseRagVariant):
    name = "llamaindex_basic"

    def __init__(self, persist_dir: str | None = None) -> None:
        from llama_index.core.postprocessor.llm_rerank import LLMRerank
        from llama_index.core.response_synthesizers import CompactAndRefine
        from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, FilterOperator
        from llama_index.llms.openai import OpenAI
        from src.adk_chatbot.knowledge_base_llamaindex import (
            DEFAULT_LLAMAINDEX_DIR,
            load_llamaindex_index,
        )

        self.persist_dir = persist_dir or os.getenv("LLAMAINDEX_PERSIST_DIR", DEFAULT_LLAMAINDEX_DIR)
        self.index = load_llamaindex_index(self.persist_dir)
        self._top_k = int(os.getenv("LLAMAINDEX_TOP_K", "8"))
        self._rerank_top_n = int(os.getenv("LLAMAINDEX_RERANK_TOP_N", "5"))
        llm_model = os.getenv("LLAMAINDEX_LLM", "gpt-4.1-mini")
        self._llm = OpenAI(model=llm_model)
        self._reranker = LLMRerank(top_n=self._rerank_top_n, llm=self._llm)
        self._synthesizer = CompactAndRefine(llm=self._llm, streaming=False)
        self._MetadataFilter = MetadataFilter
        self._MetadataFilters = MetadataFilters
        self._FilterOperator = FilterOperator

    def query(self, query_str: str) -> Dict[str, Any]:
        if self._is_code_query(query_str):
            filters = self._MetadataFilters(
                filters=[
                    self._MetadataFilter(
                        key="is_code",
                        value="true",
                        operator=self._FilterOperator.EQ,
                    )
                ]
            )
            query_engine = self.index.as_query_engine(
                similarity_top_k=self._top_k,
                filters=filters,
                node_postprocessors=[self._reranker],
                response_synthesizer=self._synthesizer,
            )
        else:
            query_engine = self.index.as_query_engine(
                similarity_top_k=self._top_k,
                node_postprocessors=[self._reranker],
                response_synthesizer=self._synthesizer,
            )

        response = query_engine.query(query_str)
        answer = str(response)

        contexts: List[str] = []
        if hasattr(response, "source_nodes") and response.source_nodes:
            for node in response.source_nodes:
                try:
                    if hasattr(node, "node") and hasattr(node.node, "get_content"):
                        contexts.append(node.node.get_content())
                    elif hasattr(node, "get_content"):
                        contexts.append(node.get_content())
                    elif hasattr(node, "text"):
                        contexts.append(node.text)
                except Exception:
                    continue

        if not contexts:
            return {"answer": "Not found in the provided documentation.", "contexts": contexts}
        if self._is_code_query(query_str):
            code_blocks = self._extract_code_blocks(contexts)
            if not code_blocks:
                return {"answer": "Not found in the provided documentation.", "contexts": contexts}
            answer = "```python\n" + "\n\n".join(code_blocks) + "\n```"
            return {"answer": answer, "contexts": contexts}

        return {"answer": answer, "contexts": contexts}


RAG_VARIANTS = {
    AgnoRerankRag.name: AgnoRerankRag,
    FusionRag.name: FusionRag,
    LlamaIndexRag.name: LlamaIndexRag,
}
