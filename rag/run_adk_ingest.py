import argparse
from pathlib import Path

from dotenv import load_dotenv

from adk_rag import load_config, run_ingestion


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Ingest ADK docs into a local FAISS index with hybrid retrieval support."
    )
    parser.add_argument("--config", help="Path to config YAML", default=None)
    parser.add_argument("--docs-path", help="Override docs path", default=None)
    parser.add_argument("--index-path", help="Override index path", default=None)
    parser.add_argument("--embedding-model", help="Override embedding model", default=None)
    parser.add_argument("--chunk-size", type=int, help="Override chunk size", default=None)
    parser.add_argument("--chunk-overlap", type=int, help="Override chunk overlap", default=None)
    parser.add_argument(
        "--no-hybrid",
        action="store_true",
        help="Disable hybrid retrieval (use legacy vector-only mode)",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    if args.docs_path:
        config.docs_path = str(Path(args.docs_path).expanduser())
    if args.index_path:
        config.index_path = str(Path(args.index_path).expanduser())
    if args.embedding_model:
        config.embedding_model = args.embedding_model
    if args.chunk_size:
        config.chunk_size = args.chunk_size
    if args.chunk_overlap:
        config.chunk_overlap = args.chunk_overlap
    if args.no_hybrid:
        config.use_hybrid_retrieval = False

    print("=" * 50)
    print("ADK RAG Ingestion")
    print("=" * 50)
    print(f"Provider: {config.llm_provider}")
    print(f"Docs path: {config.docs_path}")
    print(f"Index path: {config.index_path}")
    print(f"Embedding model: {config.embedding_model}")
    print(f"Chunk size: {config.chunk_size}")
    print(f"Chunk overlap: {config.chunk_overlap}")
    print(f"Hybrid retrieval: {config.use_hybrid_retrieval}")
    print("=" * 50)

    count = run_ingestion(config)
    if count == 0:
        print("No documents ingested. Check the docs path.")
    else:
        print(f"Successfully ingested {count} chunks.")
        if config.use_hybrid_retrieval:
            print("Created: FAISS index, parent docs, BM25 data")


if __name__ == "__main__":
    main()
