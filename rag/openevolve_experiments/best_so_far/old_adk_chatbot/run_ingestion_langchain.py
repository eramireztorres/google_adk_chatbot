import os
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import LanceDB
import lancedb
from langchain_core.documents import Document

from src.adk_chatbot.knowledge_base_langchain import (
    DEFAULT_LC_DB_PATH,
    DEFAULT_LC_TABLE_NAME,
)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


def main() -> None:
    docs_path = "/home/erick/repo/adk_chatbot/docs/adk_docs"
    if not os.path.exists(docs_path):
        print(f"Error: Docs directory not found at {docs_path}")
        return

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    loader = DirectoryLoader(
        docs_path,
        glob="**/*.md",
        loader_cls=TextLoader,
        recursive=True,
        silent_errors=True,
    )
    docs = loader.load()

    code_docs = []
    prose_docs = []
    code_pattern = re.compile(r"```.*?```", re.DOTALL)

    for doc in docs:
        source = doc.metadata.get("source")
        text = doc.page_content or ""
        if not text:
            continue

        for match in code_pattern.findall(text):
            code_docs.append(
                Document(
                    page_content=match.strip(),
                    metadata={"source": source, "type": "code"},
                )
            )

        prose = code_pattern.sub("", text).strip()
        if prose:
            prose_docs.append(
                Document(
                    page_content=prose,
                    metadata={"source": source, "type": "prose"},
                )
            )

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=120)
    prose_splits = splitter.split_documents(prose_docs)
    splits = prose_splits + code_docs

    conn = lancedb.connect(DEFAULT_LC_DB_PATH)
    if DEFAULT_LC_TABLE_NAME in conn.table_names():
        conn.drop_table(DEFAULT_LC_TABLE_NAME)

    LanceDB.from_documents(
        splits,
        embeddings,
        connection=conn,
        table_name=DEFAULT_LC_TABLE_NAME,
    )

    print(
        "--- LangChain ingestion complete ---\n"
        f"Docs loaded: {len(docs)}\n"
        f"Chunks stored: {len(splits)}\n"
        f"DB path: {DEFAULT_LC_DB_PATH}\n"
        f"Table: {DEFAULT_LC_TABLE_NAME}"
    )


if __name__ == "__main__":
    main()
