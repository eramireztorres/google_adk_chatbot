# Google ADK Chatbot

A specialized assistant for [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) documentation. This is **not a general-purpose chatbot** - it is purpose-built to provide accurate, grounded answers about Google ADK APIs, patterns, and best practices by retrieving information directly from the official documentation.

---

## 1. Installation

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

---

## 2. Environment Setup

Create a local `.env` file in the root directory to supply API keys and configuration. **This is required before ingestion or running the system.**

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

> [!NOTE]
> `GOOGLE_API_KEY` is still required for the ADK web interface, but the RAG system will use OpenAI if configured.

### Full Configuration Reference

For more advanced configuration (switching providers, models, or retrieval settings), see the [Configuration Guide](#full-configuration-reference-below).

---

## 3. Mandatory Step: Data Ingestion

Before you can query the chatbot, you **must** ingest the documentation into the local vector index. This process converts the ADK documentation into a searchable format.

> [!IMPORTANT]
> You must have your `.env` file configured with API keys before running this step.

You can use either the CLI command or the Python script:

```bash
# Using the CLI (preferred)
adk-rag-ingest

# OR using the Python script
python rag/run_adk_ingest.py
```

---

## 4. Usage Options

Once ingestion is complete, you can choose how to run the system.

### Option A: RAG Pipeline via MCP Server (Tool Mode)

Run just the RAG MCP server to integrate it into your own agent or application. The server exposes a `get_adk_info(query)` tool via the Model Context Protocol (MCP).

```bash
# Using the CLI
adk-rag-server --port 8001

# OR using the Python script
python rag/run_adk_mcp_server.py --port 8001
```

Access the server at `http://localhost:8001/sse`.

### Option B: Full Multi-Agent Chatbot (UI Mode)

Run the complete chatbot system with a web interface and a multi-agent pipeline (Planning, Retrieval, Code Validation, Synthesis).

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

## Full Configuration Reference

The following variables can be set in your `.env` file:

```bash
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
RAG_RERANK_MODEL=gpt-4.1-mini

# Temperature for LLM responses (0.0 = deterministic)
RAG_TEMPERATURE=0.0

# Enable/disable features
RAG_USE_HYBRID=true
RAG_USE_RERANKING=true

# Server Ports
MCP_PORT=8001
ADK_WEB_PORT=8000
```

### Provider Auto-Detection

| Provider | Requirement | Default LLM | Default Embeddings |
|----------|-------------|-------------|-------------------|
| **OpenAI** | `OPENAI_API_KEY` | `gpt-4.1-mini` | `text-embedding-3-large` |
| **Google** | `GOOGLE_API_KEY` | `gemini-2.5-flash-lite` | `models/text-embedding-004` |

---

## RAG Pipeline Features

- **Hybrid retrieval**: FAISS vector search + BM25 for better recall.
- **LLM reranking**: Scores and ranks chunks by relevance to the query.
- **Parent-child chunking**: Headers define parent documents; smaller child chunks for precise retrieval.
- **Cross-language filtering**: Detects requested programming language (Python, Go, Java) and filters results.
- **Strict grounding**: Answers are generated only from retrieved documentation - no hallucination.

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
