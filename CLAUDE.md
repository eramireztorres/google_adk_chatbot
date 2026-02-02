# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAG-based MCP server and multi-agent chatbot for querying Google ADK (Agent Development Kit) documentation. The system uses a RAG pipeline exposed via MCP (Model Context Protocol) and a multi-agent orchestration layer built with Google ADK.

## Development Commands

### Environment Setup
```bash
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows
pip install -e .                  # Editable install (recommended)
```

### Running Tests
```bash
pytest                          # Run all tests
pytest tests/test_config.py     # Run specific test file
pytest tests/test_query.py -v   # Verbose output
```

Tests use mocked embeddings (FakeEmbeddings) and LLM (DummyLLM) from `tests/conftest.py` - no API keys required for testing.

### One-Time Setup: Ingest Documentation
```bash
python rag/run_adk_ingest.py
```

### Start MCP Server
```bash
python rag/run_adk_mcp_server.py --port 8001
```

### Start Full Development Environment
```bash
bash scripts/run_adk_dev.sh       # Linux/macOS
scripts\run_adk_dev.bat           # Windows CMD
.\scripts\run_adk_dev.ps1         # Windows PowerShell
```
Starts MCP server (port 8001) + ADK web interface (port 8000).

### Entry Points (after pip install -e .)
```bash
adk-rag-ingest   # Document ingestion
adk-rag-server   # MCP server
```

## Architecture

### Two Main Components

1. **RAG System** (`rag/adk_rag/`)
   - `config.py`: RAGConfig dataclass, loads from `config.yaml` + env vars, auto-detects provider
   - `ingest.py`: Document ingestion pipeline
   - `chunking.py`: Custom chunking (separates code blocks, removes nav noise, splits by headers)
   - `query.py`: RAGSystem class - hybrid retrieval (FAISS + BM25), LLM reranking, answer generation
   - Vector store: FAISS (index stored in `rag/adk_rag/index/`)

2. **Agent System** (`chatbot/ADK_assistant/agent.py`)
   - Multi-agent pipeline using Google ADK agent types
   - Root coordinator invokes a RAG workflow loop

### Agent Pipeline Flow

```
RootAgent (LlmAgent)
  └── RagAgentLoop (LoopAgent, max 2 iterations)
        └── RagAgentPipeline (SequentialAgent)
              ├── PlanningAgent: splits complex queries into subqueries
              ├── QueryAgent: calls RAG MCP tool (get_adk_info)
              ├── CodeCheckAgent: validates Python code blocks
              └── SynthesizerAgent: produces final answer
```

### MCP Integration

- RAG exposed as MCP tool via `MCPToolset` with SSE transport
- Tool: `get_adk_info(query: str)` returns `{answer, contexts, sources}`
- Default URL: `http://localhost:8001/sse`

### Configuration

Environment variables override `rag/adk_rag/config.yaml`. Required: `OPENAI_API_KEY` or `GOOGLE_API_KEY`.

**Provider Auto-Detection** (in order of precedence):
1. `RAG_LLM_PROVIDER` / `ADK_LLM_PROVIDER` env var explicitly set
2. `OPENAI_API_KEY` present → OpenAI
3. `GOOGLE_API_KEY` present → Google
4. `OLLAMA_API_BASE` present → Ollama

**Key Environment Variables:**
| Variable | Description | Default |
|----------|-------------|---------|
| `RAG_LLM_PROVIDER` | Provider for RAG (`openai`, `google`, `ollama`) | auto-detect |
| `RAG_LLM_MODEL` | LLM for RAG answers | gpt-4.1-mini / gemini-2.5-flash-lite |
| `RAG_EMBEDDING_MODEL` | Embedding model | text-embedding-3-large / text-embedding-004 |
| `ADK_LLM_MODEL` | LLM for agent system | gpt-4.1-mini / gemini-2.5-flash-lite |
| `RAG_MCP_URL` | MCP server endpoint | http://localhost:8001/sse |
| `MCP_PORT` | RAG server port | 8001 |
| `ADK_WEB_PORT` | Web UI port | 8000 |

## Key Patterns

### Agent Creation
Uses Google ADK agent types with LiteLLM wrapper:
```python
from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(model=f"openai/{model_name}")
agent = LlmAgent(name="...", model=model, instruction="...", tools=[...])
```

### Tool Safety
Code snippet runner (`run_python_snippet`) restricts:
- Dangerous imports: os, sys, subprocess, open, exec, eval
- Max snippet size: 1000 chars
- Timeout: 5 seconds
- Sets `tool_context.actions.escalate = True` on failure to exit loops early

### Test Fixtures
`tests/conftest.py` provides:
- `FakeEmbeddings`: Deterministic 8D vectors from hash
- `DummyLLM`: Returns fixed content for mocking

## Coding Conventions

- Python 3.10+, PEP 8 with 4-space indentation
- Type hints throughout (`from __future__ import annotations`)
- Verb-based script names: `run_ingestion.py`, `validate_setup.py`
- Config files in YAML near the scripts that use them
- Commit messages: short, past-tense sentences
