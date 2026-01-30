import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route, Mount
from dotenv import load_dotenv

from src.adk_chatbot.rag_variants import RAG_VARIANTS, BaseRagVariant

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

if not os.getenv("OPENAI_API_KEY"):
    print("CRITICAL: OPENAI_API_KEY missing in rag_server environment!")
else:
    k = os.getenv("OPENAI_API_KEY")
    print(f"DEBUG: rag_server found OPENAI_API_KEY: {k[:5]}...{k[-5:]}")

# Initialize FastMCP
mcp = FastMCP("adk_rag_server")

# Global RAG variant instance
_rag_instance: BaseRagVariant | None = None


def get_rag_instance() -> BaseRagVariant:
    global _rag_instance
    if _rag_instance is None:
        variant = os.getenv("RAG_VARIANT", "agno_rerank")
        if variant not in RAG_VARIANTS:
            raise ValueError(f"Unknown RAG_VARIANT '{variant}'. Options: {list(RAG_VARIANTS)}")
        print(f"Initializing RAG variant: {variant}")
        _rag_instance = RAG_VARIANTS[variant]()
    return _rag_instance


@mcp.tool()
def list_rag_variants() -> dict:
    """Returns the available RAG variants and the active one."""
    return {
        "active": os.getenv("RAG_VARIANT", "agno_rerank"),
        "available": list(RAG_VARIANTS.keys()),
    }


@mcp.tool()
def get_adk_info(query: str) -> dict:
    """
    Retrieves information about Google AdK framework using the configured RAG variant.
    Use this tool when you need to answer technical questions about AdK agents, tools, configuration, etc.

    Args:
        query (str): The search query or question about AdK.

    Returns:
        dict: A dictionary containing the 'answer' and 'contexts'.
    """
    try:
        rag = get_rag_instance()
        return rag.query(query)
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def get_adk_info_variant(query: str, variant: str) -> dict:
    """
    Retrieves information using a specific RAG variant without changing the global default.

    Args:
        query (str): The search query or question about AdK.
        variant (str): The RAG variant name.

    Returns:
        dict: A dictionary containing the 'answer' and 'contexts'.
    """
    try:
        if variant not in RAG_VARIANTS:
            return {"status": "error", "message": f"Unknown variant: {variant}"}
        return RAG_VARIANTS[variant]().query(query)
    except Exception as e:
        return {"status": "error", "message": str(e)}


sse = SseServerTransport("/messages/")


async def handle_sse(request: Request):
    async with sse.connect_sse(
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
        Mount("/messages/", app=sse.handle_post_message),
    ],
)


def run():
    print("Starting AdK RAG MCP Server on port 8000...")
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    run()
