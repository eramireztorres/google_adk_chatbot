from pathlib import Path

from rag.adk_rag.chunking import chunk_document, load_documents


def test_chunk_document_splits_code_and_text():
    text = """# Title\n\nIntro text.\n\n```python\ndef foo():\n    return 1\n```\n\nMore text."""
    chunks = chunk_document(text, "source.md", chunk_size=1000, chunk_overlap=100)
    types = [chunk.metadata.get("type") for chunk in chunks]
    assert "code" in types
    assert "text" in types


def test_load_documents_skips_navigation(tmp_path: Path):
    doc_path = tmp_path / "doc.md"
    doc_path.write_text("Skip to main content\nNavigation\nActual content.", encoding="utf-8")

    docs = load_documents(str(tmp_path), chunk_size=1000, chunk_overlap=100)
    # The navigation chunk should be skipped, leaving only real content
    assert any("Actual content" in doc.page_content for doc in docs)
    assert all("Skip to main content" not in doc.page_content for doc in docs)
