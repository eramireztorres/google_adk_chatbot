
import os
from typing import Dict, Any, List
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from google.adk.tools.tool_context import ToolContext

from src.adk_chatbot.knowledge_base import get_knowledge_base

# Adapted from docs/best_program.py to be self-contained in the package
class RAGSystem:
    def __init__(self):
        self.agent = None
        self.knowledge = None
        self._initialize_system()

    def _augment_query(self, query_str: str) -> str:
        lowered = query_str.lower()
        if any(token in lowered for token in ("example", "code", "snippet")):
            return f"{query_str} example code"
        return query_str

    def _initialize_system(self):
        # Initialize the knowledge base using the shared configuration
        self.knowledge = get_knowledge_base()

        self.agent = Agent(
            model=OpenAIChat(id="gpt-4.1-mini"),
            instruction=(
                "Answer only using the retrieved documentation context. "
                "If the answer or code is not explicitly present, say "
                "\"Not found in the provided documentation.\" "
                "Do not guess imports or APIs."
            ),
            knowledge=self.knowledge,
            search_knowledge=True,
            markdown=False,
        )

    def query(self, query_str: str) -> Dict[str, Any]:
        # DEBUG: Explicitly check knowledge base search results
        print(f"DEBUG: RAGSystem.query called with: '{query_str}'")
        search_query = self._augment_query(query_str)
        try:
            # Using defaults to avoid kwarg errors
            manual_results = self.knowledge.search(query=search_query)
            print(f"DEBUG: Manual search found {len(manual_results)} documents.")
            for i, res in enumerate(manual_results):
                print(f"DEBUG Result {i}: {res.content[:50]}...")
        except Exception as e:
            print(f"DEBUG: Manual search FAILED: {e}")
            manual_results = []

        # Agent run will use knowledge search automatically
        response_obj = self.agent.run(query_str)
        answer = response_obj.content

        contexts = []
        if hasattr(response_obj, "sources") and response_obj.sources:
            contexts = [source.content for source in response_obj.sources if hasattr(source, "content")]
            print(f"DEBUG: Agent.run returned {len(contexts)} sources.")
        else:
            print("DEBUG: Agent.run returned NO sources.")
            # FALLBACK: If agent.run fails to populate sources but we found docs, force use manual results
            # This ensures we don't return empty context if data exists.
            if manual_results:
                 print("DEBUG: Using manual results as fallback contexts.")
                 contexts = [res.content for res in manual_results]
        if manual_results:
            manual_contexts = [res.content for res in manual_results]
            contexts = list(dict.fromkeys(contexts + manual_contexts))

        if not contexts:
            answer = "Not found in the provided documentation."

        return {
            "answer": answer,
            "contexts": contexts,
        }

# Global cache for the RAG system
_rag_system_cache = None

def get_adk_info(query: str, tool_context: ToolContext) -> dict:
    """
    Retrieves information about Google AdK framework using a RAG system.
    Use this tool when you need to answer technical questions about AdK agents, tools, configuration, etc.
    
    Args:
        query (str): The search query or question about AdK.
        tool_context (ToolContext): The tool context provided by AdK.
    
    Returns:
        dict: A dictionary containing the 'answer' and 'contexts'.
    """
    global _rag_system_cache
    
    try:
        if _rag_system_cache is None:
            print(f"--- Initializing RAG System (Inference Mode) ---")
            _rag_system_cache = RAGSystem()
            
        return _rag_system_cache.query(query)
    except Exception as e:
        return {"status": "error", "message": str(e)}
