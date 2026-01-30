# Google ADK Chatbot

A specialized assistant for [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) documentation. This is **not a general-purpose chatbot** - it is purpose-built to provide accurate, grounded answers about Google ADK APIs, patterns, and best practices by retrieving information directly from the official documentation.

## Installation

```bash
# Clone the repository
git clone https://github.com/eramireztorres/google_adk_chatbot.git
cd google_adk_chatbot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

After installation, CLI commands are available:
- `adk-rag-ingest` - Ingest documentation into the vector index
- `adk-rag-server` - Start the RAG MCP server

---

## What This Project Offers

### Option 1: RAG Pipeline via MCP Server (Use in Your Own Agent)

Run just the RAG MCP server and integrate it into your own agent or application. The server exposes a `get_adk_info(query)` tool via the Model Context Protocol (MCP) that returns grounded answers with source citations.

```bash
# 1. Ingest the documentation (one-time)
python rag/run_adk_ingest.py

# 2. Start the MCP server
python rag/run_adk_mcp_server.py --port 8001
```

Then connect your agent to `http://localhost:8001/sse` using any MCP-compatible client.

### Option 2: Full Multi-Agent Chatbot

Run the complete chatbot system with a multi-agent pipeline that includes query planning, RAG retrieval, code validation, and answer synthesis.

```bash
# Linux/macOS
bash scripts/run_adk_dev.sh

# Windows (Command Prompt)
scripts\run_adk_dev.bat

# Windows (PowerShell)
.\scripts\run_adk_dev.ps1
```

Access the web interface at `http://localhost:8000`.

---

## Environment Setup

Create a local `.env` file (not committed) to supply API keys and configuration.

### Minimal Configuration (Google Only)

If you only have a Google API key:

```bash
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

This uses `gemini-2.5-flash-lite` for LLM and `models/text-embedding-004` for embeddings.

### Minimal Configuration (OpenAI Only)

If you only have an OpenAI API key:

```bash
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

This uses `gpt-4.1-mini` for LLM and `text-embedding-3-large` for embeddings.

> **Note**: `GOOGLE_API_KEY` is still required for the ADK web interface, but the RAG system will use OpenAI.

### Full Configuration (All Options)

```bash
# =============================================================================
# API KEYS (at least one LLM provider required)
# =============================================================================
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE

# =============================================================================
# RAG SYSTEM CONFIGURATION
# =============================================================================
# Provider selection: "openai" or "google"
# Auto-detected if not set: uses OpenAI if OPENAI_API_KEY exists, else Google
RAG_LLM_PROVIDER=openai

# LLM model for answer generation
# OpenAI default: gpt-4.1-mini | Google default: gemini-2.5-flash-lite
RAG_LLM_MODEL=gpt-4.1-mini

# Embedding model for vector search
# OpenAI default: text-embedding-3-large | Google default: models/text-embedding-004
RAG_EMBEDDING_MODEL=text-embedding-3-large

# LLM model for reranking retrieved chunks
# Same defaults as RAG_LLM_MODEL
RAG_RERANK_MODEL=gpt-4.1-mini

# Temperature for LLM responses (0.0 = deterministic)
RAG_TEMPERATURE=0.0

# Enable/disable hybrid retrieval (vector + BM25)
RAG_USE_HYBRID=true

# Enable/disable LLM-based reranking
RAG_USE_RERANKING=true

# =============================================================================
# AGENT SYSTEM CONFIGURATION (for full chatbot)
# =============================================================================
# Provider for the multi-agent system: "openai" or "google"
ADK_LLM_PROVIDER=openai

# Model for agent LLM calls
ADK_LLM_MODEL=gpt-4.1-mini

# Logging level: DEBUG, INFO, WARNING, ERROR
ADK_LOG_LEVEL=INFO

# =============================================================================
# LEGACY OPENAI ENV VARS (backward compatibility)
# These work when provider is "openai", but RAG_* vars take precedence
# =============================================================================
OPENAI_LLM_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
OPENAI_TEMPERATURE=0.0

# =============================================================================
# SERVER CONFIGURATION
# =============================================================================
# Port for the RAG MCP server
MCP_PORT=8001

# Port for the ADK web interface
ADK_WEB_PORT=8000

# URL for agents to connect to the RAG MCP server
RAG_MCP_URL=http://localhost:8001/sse
```

### Provider Auto-Detection

If `RAG_LLM_PROVIDER` is not explicitly set, the system auto-detects:

1. If `OPENAI_API_KEY` is set → uses **OpenAI**
2. Else if `GOOGLE_API_KEY` is set → uses **Google**
3. Default → **Google**

| Provider | Default LLM | Default Embeddings |
|----------|-------------|-------------------|
| OpenAI | `gpt-4.1-mini` | `text-embedding-3-large` |
| Google | `gemini-2.5-flash-lite` | `models/text-embedding-004` |

---

## RAG Pipeline Details

### One-Time Ingestion

Before querying, ingest the ADK documentation into the vector index:

```bash
python rag/run_adk_ingest.py
```

Optional overrides:

```bash
python rag/run_adk_ingest.py \
  --docs-path rag/docs/adk_docs \
  --index-path rag/adk_rag/index \
  --embedding-model models/text-embedding-004
```

### MCP Server

The RAG system is exposed via MCP with one tool:

- **`get_adk_info(query: str)`** - Returns `{answer, contexts, sources}`

Start the server:

```bash
python rag/run_adk_mcp_server.py --port 8001
```

Optional flags:

```bash
python rag/run_adk_mcp_server.py \
  --port 8001 \
  --llm-model gemini-2.5-flash-lite \
  --no-reranking \
  --no-hybrid
```

### RAG Pipeline Features

- **Hybrid retrieval**: FAISS vector search + BM25 for better recall
- **LLM reranking**: Scores and ranks chunks by relevance to the query
- **Parent-child chunking**: Headers define parent documents; smaller child chunks for precise retrieval
- **Cross-language filtering**: Detects requested programming language (Python, Go, Java) and filters results
- **Strict grounding**: Answers are generated only from retrieved documentation - no hallucination

---

## Full Chatbot Architecture

The multi-agent chatbot uses Google ADK's agent orchestration:

```
RootAgent (coordinator)
  └── RagAgentLoop (max 2 iterations)
        └── RagAgentPipeline (sequential)
              ├── PlanningAgent   - Splits complex queries into subqueries
              ├── QueryAgent      - Calls RAG MCP tool
              ├── CodeCheckAgent  - Validates Python code blocks
              └── SynthesizerAgent - Produces final answer
```

### Start the full system:

```bash
# Linux/macOS
bash scripts/run_adk_dev.sh

# Windows (Command Prompt)
scripts\run_adk_dev.bat

# Windows (PowerShell)
.\scripts\run_adk_dev.ps1
```

This launches:
- RAG MCP server on port `8001` (configurable via `MCP_PORT`)
- ADK web interface on port `8000` (configurable via `ADK_WEB_PORT`)
