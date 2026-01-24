from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from rag.adk_rag.config import RAGConfig
from rag.adk_rag.query import RAGSystem

from conftest import DummyLLM, FakeEmbeddings


def test_query_missing_index(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("rag.adk_rag.query.OpenAIEmbeddings", lambda model: FakeEmbeddings())
    monkeypatch.setattr("rag.adk_rag.query.ChatOpenAI", lambda model, temperature: DummyLLM())

    cfg = RAGConfig(index_path=str(tmp_path / "missing"))
    rag = RAGSystem(cfg)

    result = rag.query("test")
    assert "Vector index not found" in result["answer"]


def test_query_returns_answer(tmp_path: Path, monkeypatch):
    embeddings = FakeEmbeddings()
    docs = [Document(page_content="FunctionTool example", metadata={"source": "a.md"})]
    store = FAISS.from_documents(docs, embeddings)
    index_path = tmp_path / "index"
    store.save_local(str(index_path))

    monkeypatch.setattr("rag.adk_rag.query.OpenAIEmbeddings", lambda model: embeddings)
    monkeypatch.setattr("rag.adk_rag.query.ChatOpenAI", lambda model, temperature: DummyLLM("ANSWER"))

    cfg = RAGConfig(index_path=str(index_path))
    rag = RAGSystem(cfg)
    result = rag.query("FunctionTool")

    assert result["answer"] == "ANSWER"
    assert result["contexts"]
    assert result["sources"] == ["a.md"]
