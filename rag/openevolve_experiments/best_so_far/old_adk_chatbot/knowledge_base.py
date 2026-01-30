
import os
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.reranker.cohere import CohereReranker

from agno.db.sqlite.sqlite import SqliteDb

# Default path for persistent storage
DEFAULT_DB_PATH = "/home/erick/repo/adk_chatbot/data/lancedb"
DEFAULT_CONTENTS_DB_PATH = "/home/erick/repo/adk_chatbot/data/contents.db"

def get_vector_db(db_path: str = DEFAULT_DB_PATH) -> LanceDb:
    """
    Creates and returns the LanceDb configuration.
    """
    # Force Vector search for stability
    # try:
    #     import tantivy
    #     search_type = SearchType.hybrid
    # except ImportError:
    #     search_type = SearchType.vector
    search_type = SearchType.vector

    reranker = None
    if os.getenv("COHERE_API_KEY"):
        reranker = CohereReranker(model="rerank-v3.5")

    return LanceDb(
        table_name="adk_docs",
        uri=db_path,
        search_type=search_type,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        reranker=reranker,
    )

def get_knowledge_base(db_path: str = DEFAULT_DB_PATH) -> Knowledge:
    """
    Creates the Knowledge object with the configured Vector DB and Contents DB.
    """
    return Knowledge(
        vector_db=get_vector_db(db_path),
        # contents_db=SqliteDb(db_file=DEFAULT_CONTENTS_DB_PATH), # Caused vector=None issue
    )
