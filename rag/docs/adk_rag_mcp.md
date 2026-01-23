# ADK RAG MCP Server

## Environment

Create a local `.env` (not committed) to supply keys and overrides:

```bash
OPENAI_API_KEY=...
OPENAI_LLM_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TEMPERATURE=0.2
```

If you do not create a `.env`, the defaults in `rag/adk_rag/config.yaml` are used.
The only required runtime setting is `OPENAI_API_KEY`, which must be present in
the environment for OpenAI calls to succeed.

## One-time ingestion

```bash
python rag/run_adk_ingest.py
```

To override paths:

```bash
python rag/run_adk_ingest.py --docs-path rag/docs/adk_docs --index-path rag/adk_rag/index
```

## Run the MCP server

```bash
python rag/run_adk_mcp_server.py --port 8000
```

To override the index path:

```bash
python rag/run_adk_mcp_server.py --index-path rag/adk_rag/index --port 8001
```

## Config

Defaults live in `rag/adk_rag/config.yaml` and can be overridden with `--config`.
