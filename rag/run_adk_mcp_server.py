import argparse

import uvicorn
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route

from adk_rag import load_config
from adk_rag.query import RAGSystem

mcp = FastMCP("adk_rag_server")
_sse_transport = SseServerTransport("/messages/")
_rag_system: RAGSystem | None = None
_config = None


def get_rag_system() -> RAGSystem:
    global _rag_system
    if _config is None:
        raise RuntimeError("RAG config not loaded.")
    if _rag_system is None:
        _rag_system = RAGSystem(_config)
    return _rag_system


@mcp.tool()
def get_adk_info(query: str) -> dict:
    """
    Retrieve information about Google ADK using the local RAG index.

    Args:
        query: The question about Google ADK.
    """
    try:
        rag = get_rag_system()
        return rag.query(query)
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


async def handle_sse(request: Request):
    async with _sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as (reader, writer):
        await mcp._mcp_server.run(
            reader,
            writer,
            mcp._mcp_server.create_initialization_options(),
        )
    return Response()


app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=_sse_transport.handle_post_message),
    ],
)


def main() -> None:
    global _config
    load_dotenv()

    parser = argparse.ArgumentParser(description="Run the ADK RAG MCP server.")
    parser.add_argument("--config", help="Path to config YAML", default=None)
    parser.add_argument("--index-path", help="Override index path", default=None)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--llm-model", help="Override LLM model", default=None)
    parser.add_argument("--embedding-model", help="Override embedding model", default=None)
    parser.add_argument("--temperature", type=float, help="Override model temperature", default=None)
    parser.add_argument(
        "--no-hybrid",
        action="store_true",
        help="Disable hybrid retrieval (use legacy vector-only mode)",
    )
    parser.add_argument(
        "--no-reranking",
        action="store_true",
        help="Disable LLM reranking",
    )
    args = parser.parse_args()

    _config = load_config(args.config)
    if args.index_path:
        _config.index_path = args.index_path
    if args.llm_model:
        _config.llm_model = args.llm_model
    if args.embedding_model:
        _config.embedding_model = args.embedding_model
    if args.temperature is not None:
        _config.temperature = args.temperature
    if args.no_hybrid:
        _config.use_hybrid_retrieval = False
    if args.no_reranking:
        _config.use_llm_reranking = False

    print("=" * 50)
    print("ADK RAG MCP Server")
    print("=" * 50)
    print(f"Provider: {_config.llm_provider}")
    print(f"Host: {args.host}:{args.port}")
    print(f"Index path: {_config.index_path}")
    print(f"LLM model: {_config.llm_model}")
    print(f"Embedding model: {_config.embedding_model}")
    print(f"Hybrid retrieval: {_config.use_hybrid_retrieval}")
    print(f"LLM reranking: {_config.use_llm_reranking}")
    print("=" * 50)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
