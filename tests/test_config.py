from pathlib import Path

from rag.adk_rag.config import load_config


def test_config_env_overrides(monkeypatch, tmp_path: Path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "docs_path: ../docs\nindex_path: ./index\nllm_model: default-llm\nembedding_model: default-embed\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("OPENAI_LLM_MODEL", "override-llm")
    monkeypatch.setenv("OPENAI_EMBEDDING_MODEL", "override-embed")
    monkeypatch.setenv("OPENAI_TEMPERATURE", "0.7")

    cfg = load_config(str(config_path))

    assert cfg.llm_model == "override-llm"
    assert cfg.embedding_model == "override-embed"
    assert cfg.temperature == 0.7
    assert Path(cfg.docs_path).is_absolute()
    assert Path(cfg.index_path).is_absolute()
