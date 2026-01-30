from pathlib import Path

from rag.adk_rag.config import load_config


def test_config_env_overrides(monkeypatch, tmp_path: Path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "docs_path: ../docs\nindex_path: ./index\nllm_model: default-llm\nembedding_model: default-embed\n",
        encoding="utf-8",
    )

    # Use the provider-agnostic RAG_* env vars
    monkeypatch.setenv("RAG_LLM_MODEL", "override-llm")
    monkeypatch.setenv("RAG_EMBEDDING_MODEL", "override-embed")
    monkeypatch.setenv("RAG_TEMPERATURE", "0.7")

    cfg = load_config(str(config_path))

    assert cfg.llm_model == "override-llm"
    assert cfg.embedding_model == "override-embed"
    assert cfg.temperature == 0.7
    assert Path(cfg.docs_path).is_absolute()
    assert Path(cfg.index_path).is_absolute()


def test_config_openai_env_with_provider(monkeypatch, tmp_path: Path):
    """Test that OpenAI env vars work when provider is openai."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "docs_path: ../docs\nindex_path: ./index\n",
        encoding="utf-8",
    )

    # Set OPENAI_API_KEY to trigger openai provider detection
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_LLM_MODEL", "gpt-4-turbo")
    monkeypatch.setenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    cfg = load_config(str(config_path))

    assert cfg.llm_provider == "openai"
    assert cfg.llm_model == "gpt-4-turbo"
    assert cfg.embedding_model == "text-embedding-3-small"


def test_config_google_provider_detection(monkeypatch, tmp_path: Path):
    """Test that Google provider is detected when only GOOGLE_API_KEY is set."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "docs_path: ../docs\nindex_path: ./index\n",
        encoding="utf-8",
    )

    # Ensure no OPENAI_API_KEY
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key")

    cfg = load_config(str(config_path))

    assert cfg.llm_provider == "google"
    # Check defaults are applied
    assert cfg.llm_model == "gemini-2.5-flash-lite"
    assert cfg.embedding_model == "models/text-embedding-004"
