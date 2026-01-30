import os
import lancedb
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import LanceDB

DEFAULT_LC_DB_PATH = "/home/erick/repo/adk_chatbot/data/lancedb_langchain"
DEFAULT_LC_TABLE_NAME = "adk_docs_langchain"


def get_langchain_vector_store(
    db_path: str = DEFAULT_LC_DB_PATH,
    table_name: str = DEFAULT_LC_TABLE_NAME,
    embeddings: OpenAIEmbeddings | None = None,
) -> LanceDB:
    """Return a persistent LanceDB-backed LangChain vector store."""
    if embeddings is None:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    conn = lancedb.connect(db_path)
    if table_name not in conn.table_names():
        raise FileNotFoundError(
            f"LanceDB table '{table_name}' not found in {db_path}. "
            "Run run_ingestion_langchain.py first."
        )

    return LanceDB(connection=conn, table_name=table_name, embedding=embeddings)
