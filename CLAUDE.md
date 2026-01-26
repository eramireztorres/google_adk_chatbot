# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAG-based MCP server and multi-agent chatbot for querying Google ADK (Agent Development Kit) documentation. The system uses a RAG pipeline exposed via MCP (Model Context Protocol) and a multi-agent orchestration layer built with Google ADK.

## Development Commands

### Environment Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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
bash scripts/run_adk_dev.sh  # Starts MCP server + ADK web interface
```

### Entry Points (after pip install -e .)
```bash
adk-rag-ingest   # Document ingestion
adk-rag-server   # MCP server
```

## Architecture

### Two Main Components

1. **RAG System** (`rag/adk_rag/`)
   - `config.py`: RAGConfig dataclass, loads from `config.yaml` + env vars
   - `ingest.py`: Document ingestion pipeline
   - `chunking.py`: Custom chunking (separates code blocks, removes nav noise, splits by headers)
   - `query.py`: RAGSystem class - loads FAISS index, retrieves docs, generates answers
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

Environment variables override `rag/adk_rag/config.yaml`. Required: `OPENAI_API_KEY`. Key vars:
- `ADK_LLM_MODEL`: Model for agents (default: gpt-4.1-mini)
- `OPENAI_EMBEDDING_MODEL`: Embedding model (default: text-embedding-3-small)
- `RAG_MCP_URL`: MCP server endpoint
- `MCP_PORT`, `ADK_WEB_PORT`: Server ports

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
