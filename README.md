# google_adk_chatbot
Your google-adk assistant.

## ADK RAG MCP Server

### Environment

Create a local `.env` (not committed) to supply keys and overrides:

```bash
OPENAI_API_KEY=...
OPENAI_LLM_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TEMPERATURE=0.2
ADK_LLM_PROVIDER=openai
ADK_LLM_MODEL=gpt-4.1-mini
GOOGLE_API_KEY=...
GOOGLE_GENAI_USE_VERTEXAI=FALSE
MCP_PORT=8001
ADK_WEB_PORT=8000
RAG_MCP_URL=http://localhost:8001/sse
```

If you do not create a `.env`, the defaults in `rag/adk_rag/config.yaml` are used.
The only required runtime setting is `OPENAI_API_KEY`, which must be present in
the environment for OpenAI calls to succeed.

### One-time ingestion

```bash
python rag/run_adk_ingest.py
```

Optional overrides:

```bash
python rag/run_adk_ingest.py --docs-path rag/docs/adk_docs --index-path rag/adk_rag/index --embedding-model text-embedding-3-small
```

### Run the MCP server

```bash
python rag/run_adk_mcp_server.py --port 8000
```

Optional overrides:

```bash
python rag/run_adk_mcp_server.py --port 8000 --llm-model gpt-4.1-mini --embedding-model text-embedding-3-small --temperature 0.2
```
