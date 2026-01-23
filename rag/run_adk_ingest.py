import argparse
from pathlib import Path

from dotenv import load_dotenv

from adk_rag import load_config, run_ingestion


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Ingest ADK docs into a local FAISS index.")
    parser.add_argument("--config", help="Path to config YAML", default=None)
    parser.add_argument("--docs-path", help="Override docs path", default=None)
    parser.add_argument("--index-path", help="Override index path", default=None)
    parser.add_argument("--embedding-model", help="Override embedding model", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.docs_path:
        config.docs_path = str(Path(args.docs_path).expanduser())
    if args.index_path:
        config.index_path = str(Path(args.index_path).expanduser())
    if args.embedding_model:
        config.embedding_model = args.embedding_model

    print(f"Docs path: {config.docs_path}")
    print(f"Index path: {config.index_path}")

    count = run_ingestion(config)
    if count == 0:
        print("No documents ingested. Check the docs path.")
    else:
        print(f"Ingested {count} chunks.")


if __name__ == "__main__":
    main()
