import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.node_parser.text.code import CodeSplitter
from llama_index.core.schema import TextNode, Document

from src.adk_chatbot.knowledge_base_llamaindex import (
    DEFAULT_LLAMAINDEX_DIR,
    configure_llamaindex_settings,
)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


def _chunk_text(text: str, max_chars: int, overlap: int):
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + max_chars, text_len)
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        if end == text_len:
            break
        start = max(0, end - overlap)
    return chunks


def _split_markdown_with_code(text: str):
    segments = []
    buffer = []
    code_lines = []
    in_code = False
    code_lang = ""

    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = line.strip()
            if not in_code:
                if buffer:
                    segments.append(("text", "\n".join(buffer), ""))
                    buffer = []
                in_code = True
                code_lang = fence[3:].strip()
                code_lines = [line]
            else:
                code_lines.append(line)
                segments.append(("code", "\n".join(code_lines), code_lang))
                code_lines = []
                in_code = False
                code_lang = ""
            continue

        if in_code:
            code_lines.append(line)
        else:
            buffer.append(line)

    if in_code and code_lines:
        segments.append(("code", "\n".join(code_lines), code_lang))
    if buffer:
        segments.append(("text", "\n".join(buffer), ""))

    return segments


def main() -> None:
    docs_path = "/home/erick/repo/adk_chatbot/docs/adk_docs"
    persist_dir = os.getenv("LLAMAINDEX_PERSIST_DIR", DEFAULT_LLAMAINDEX_DIR)

    if not os.path.isdir(docs_path):
        print(f"Error: Docs directory not found at {docs_path}")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("CRITICAL ERROR: OPENAI_API_KEY is NOT set.")
        return

    configure_llamaindex_settings()

    print(f"--- Starting LlamaIndex ingestion from {docs_path} ---")
    documents = SimpleDirectoryReader(input_dir=docs_path, recursive=True).load_data()

    chunk_size = int(os.getenv("LLAMAINDEX_CHUNK_SIZE", "1024"))
    chunk_overlap = int(os.getenv("LLAMAINDEX_CHUNK_OVERLAP", "128"))
    code_chunk_chars = int(os.getenv("LLAMAINDEX_CODE_CHUNK_CHARS", "3000"))
    code_chunk_overlap = int(os.getenv("LLAMAINDEX_CODE_CHUNK_OVERLAP", "200"))
    prose_max_chars = int(os.getenv("LLAMAINDEX_PROSE_MAX_CHARS", "2400"))
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    markdown_parser = MarkdownNodeParser.from_defaults()
    code_splitter = None
    try:
        code_splitter = CodeSplitter.from_defaults(language="python")
    except Exception as exc:
        print(f"WARNING: CodeSplitter unavailable, falling back to char chunks. ({exc})")

    nodes = []
    for doc in documents:
        text = doc.get_content()
        metadata = dict(doc.metadata or {})
        source = metadata.get("file_path") or metadata.get("file_name") or metadata.get("source") or ""
        if source:
            metadata["source"] = source

        segments = _split_markdown_with_code(text)
        for seg_type, seg_text, seg_lang in segments:
            if not seg_text.strip():
                continue
            if seg_type == "code":
                if code_splitter and (seg_lang in ("python", "py", "") or seg_lang is None):
                    try:
                        code_chunks = code_splitter.split_text(seg_text)
                    except Exception:
                        code_chunks = _chunk_text(
                            seg_text,
                            max_chars=code_chunk_chars,
                            overlap=code_chunk_overlap,
                        )
                else:
                    code_chunks = _chunk_text(
                        seg_text,
                        max_chars=code_chunk_chars,
                        overlap=code_chunk_overlap,
                    )
                for chunk in code_chunks:
                    meta = dict(metadata)
                    meta["is_code"] = "true"
                    if seg_lang:
                        meta["code_language"] = seg_lang
                    nodes.append(TextNode(text=chunk, metadata=meta))
            else:
                meta = dict(metadata)
                meta["is_code"] = "false"
                temp_doc = Document(text=seg_text, metadata=meta)
                md_nodes = markdown_parser.get_nodes_from_documents([temp_doc])
                for md_node in md_nodes:
                    content = md_node.get_content()
                    if len(content) > prose_max_chars:
                        temp_md_doc = Document(text=content, metadata=md_node.metadata)
                        nodes.extend(splitter.get_nodes_from_documents([temp_md_doc]))
                    else:
                        nodes.append(TextNode(text=content, metadata=md_node.metadata))

    index = VectorStoreIndex(nodes)
    index.storage_context.persist(persist_dir=persist_dir)
    print(f"--- Ingestion complete. Persisted to {persist_dir} ---")


if __name__ == "__main__":
    main()
