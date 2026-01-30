from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from rag.adk_rag.config import RAGConfig
from rag.adk_rag import query as query_module

from conftest import DummyLLM, FakeEmbeddings


def test_query_missing_index(tmp_path: Path, monkeypatch):
    # Monkeypatch the factory functions
    monkeypatch.setattr(query_module, "_create_embeddings", lambda cfg: FakeEmbeddings())
    monkeypatch.setattr(query_module, "_create_llm", lambda cfg, temperature=None: DummyLLM())

    cfg = RAGConfig(index_path=str(tmp_path / "missing"))
    # Force provider to avoid auto-detection issues in test
    cfg.llm_provider = "openai"
    cfg.embedding_model = "test"
    cfg.llm_model = "test"

    rag = query_module.RAGSystem(cfg)

    result = rag.query("test")
    assert "Vector index not found" in result["answer"]


def test_query_returns_answer(tmp_path: Path, monkeypatch):
    embeddings = FakeEmbeddings()
    docs = [Document(page_content="FunctionTool example", metadata={"source": "a.md"})]
    store = FAISS.from_documents(docs, embeddings)
    index_path = tmp_path / "index"
    store.save_local(str(index_path))

    # Monkeypatch the factory functions
    monkeypatch.setattr(query_module, "_create_embeddings", lambda cfg: embeddings)
    monkeypatch.setattr(query_module, "_create_llm", lambda cfg, temperature=None: DummyLLM("ANSWER"))

    cfg = RAGConfig(index_path=str(index_path))
    # Force legacy mode for simpler testing and set provider
    cfg.use_hybrid_retrieval = False
    cfg.llm_provider = "openai"
    cfg.embedding_model = "test"
    cfg.llm_model = "test"

    rag = query_module.RAGSystem(cfg)
    result = rag.query("FunctionTool")

    assert result["answer"] == "ANSWER"
    assert result["contexts"]
    assert result["sources"] == ["a.md"]
