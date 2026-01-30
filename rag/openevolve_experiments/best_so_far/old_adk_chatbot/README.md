# ADK Chatbot (Core Package)

This directory contains the primary implementation of the ADK chatbot: RAG ingestion and retrieval, the MCP RAG server, the ADK agent team, API backend, and the Streamlit UI.

## Quick Start

- Install dependencies: `pip install -r requirements.txt`
- Build the knowledge base: `python3 -m src.adk_chatbot.run_ingestion`
- Start all services: `./run_all.sh`

## Service Entry Points

- CLI chat runner: `python3 -m src.adk_chatbot.main`
- MCP RAG server: `python3 -m src.adk_chatbot.rag_server`
- API backend (FastAPI): `python3 -m src.adk_chatbot.chatbot_backend`
- Streamlit UI: `streamlit run src/adk_chatbot/ui.py --server.headless true`

## RAG Architecture

The MCP server exposes `get_adk_info` as a tool for retrieving ADK documentation answers. The active RAG implementation is selected by `RAG_VARIANT`.

Current variants live in `rag_variants.py`:
- `agno_rerank`: Agentic RAG with LanceDB and optional reranking.
- `fusion_rrf`: Multi-query retrieval + RRF fusion + context-only answering.

Environment controls:
- `RAG_VARIANT` (e.g., `RAG_VARIANT=fusion_rrf ./run_all.sh`)
- `RAG_RERANKER`: `cohere`, `sentence_transformer`, `infinity`, `none`
- `RAG_FUSION_QUERIES`, `RAG_FUSION_TOP_K`, `RAG_FUSION_TOP_N`, `RAG_FUSION_RRF_K`
- `RAG_LOG_CONTEXTS=1` for retrieval debugging

## Ingestion

- `run_ingestion.py` builds the main LanceDB index from `docs/adk_docs/` into `data/lancedb/`.
- `run_ingestion_langchain.py` builds a secondary index used by the LangChain prototype.

Re-run ingestion after updating docs:
- `python3 -m src.adk_chatbot.run_ingestion`

## Agents and Backend Flow

- `agents.py` wires the root agent and the MCP-backed `rag_agent`.
- `chatbot_backend.py` exposes `/chat` and can run in RAG-only mode:
  - `RAG_ONLY_MODE=1 python3 -m src.adk_chatbot.chatbot_backend`

## Module Map

- `agents.py`: Root agent + RAG sub-agent + callbacks
- `rag_server.py`: MCP server exposing `get_adk_info`
- `rag_variants.py`: Pluggable RAG implementations
- `knowledge_base.py`: Agno/LanceDB ingestion setup
- `knowledge_base_langchain.py`: LangChain ingestion setup
- `run_ingestion.py`: Main ingestion entrypoint
- `run_ingestion_langchain.py`: LangChain ingestion entrypoint
- `chatbot_backend.py`: FastAPI backend
- `ui.py`: Streamlit UI
- `main.py`: CLI runner

## Notes

- Local `.env` files are loaded from `src/adk_chatbot/.env`.
- Generated data lives under `data/` and is safe to delete/rebuild.
