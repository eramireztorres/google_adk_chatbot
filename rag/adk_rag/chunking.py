from __future__ import annotations

import os
import re
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


@dataclass
class ChunkingResult:
    """Result of chunking operation containing child chunks and parent documents."""
    chunks: List[Document] = field(default_factory=list)
    parent_docs: Dict[str, Document] = field(default_factory=dict)


def _flatten_markdown_tabs(text: str) -> str:
    """Unrolls Google-style tab widgets into sequential headers with normalized language tags."""
    pattern = r'{% tab label="(.*?)" %}(.*?){% endtab %}'

    def replacement(match: re.Match) -> str:
        label = match.group(1).strip()
        content = match.group(2)
        lang_map = {
            "py": "Python",
            "python": "Python",
            "go": "Go",
            "golang": "Go",
            "java": "Java",
        }
        lang_tag = lang_map.get(label.lower(), label)
        return f"\n\n#### [{lang_tag}] {label} Implementation\n{content}\n"

    text = re.sub(r'{% tabs %}', '', text)
    text = re.sub(r'{% endtabs %}', '', text)
    return re.sub(pattern, replacement, text, flags=re.DOTALL)


def _strip_navigation_lines(text: str) -> str:
    """Remove common navigation boilerplate from text."""
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped in {"Skip to main content", "Navigation"}:
            continue
        lines.append(line)
    return "\n".join(lines)


def _detect_language_tag(content: str) -> str:
    """Detect programming language from code fences in content."""
    lang_match = re.search(r'```(\w+)', content)
    if lang_match:
        lang = lang_match.group(1).lower()
        if lang in ("python", "py"):
            return "[LANG=Python]"
        elif lang in ("go", "golang"):
            return "[LANG=Go]"
        elif lang == "java":
            return "[LANG=Java]"
        else:
            return f"[LANG={lang.capitalize()}]"
    return "[LANG=Unknown]"


def _detect_content_type(content: str) -> str:
    """Detect if content is primarily code or text."""
    return "[DOC_CODE]" if "```" in content else "[DOC_TEXT]"


def _extract_project_tags(breadcrumb: str) -> str:
    """Extract project area tags from breadcrumb navigation."""
    tags = []
    if re.search(r'\[?A2A\]?', breadcrumb, re.I):
        tags.append("[A2A]")
    if re.search(r'\[?WORKFLOW\]?', breadcrumb, re.I):
        tags.append("[WORKFLOW]")
    if re.search(r'\[?MCP\]?', breadcrumb, re.I):
        tags.append("[MCP]")
    if re.search(r'\[?AGENT\]?', breadcrumb, re.I):
        tags.append("[AGENT]")
    return " ".join(tags) if tags else "[GENERAL]"


def chunk_document_with_parents(
    text: str,
    source: str,
    chunk_size: int,
    chunk_overlap: int,
) -> Tuple[List[Document], Dict[str, Document]]:
    """
    Chunk a document using parent-child hierarchy.

    Returns:
        Tuple of (child_chunks, parent_docs_dict)
    """
    # Preprocess: flatten tabs and clean navigation
    text = _flatten_markdown_tabs(text)
    text = _strip_navigation_lines(text)

    if not text.strip():
        return [], {}

    # Split by headers to create parent documents
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
            ("####", "h4"),
        ]
    )
    parent_sections = header_splitter.split_text(text)

    # Child splitter for finer chunks
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n```", "\n\n", "\n", " ", ""],
    )

    child_chunks: List[Document] = []
    parent_docs: Dict[str, Document] = {}

    for parent in parent_sections:
        parent_id = str(uuid.uuid4())

        # Build breadcrumb from header metadata
        breadcrumb_parts = []
        for i in range(1, 5):
            header_val = parent.metadata.get(f"h{i}", "")
            if header_val:
                breadcrumb_parts.append(header_val)
        breadcrumb = " > ".join(breadcrumb_parts)

        # Extract tags
        project_tags = _extract_project_tags(breadcrumb)

        # Update parent metadata
        parent.metadata["source"] = source
        parent.metadata["breadcrumb"] = breadcrumb
        parent.metadata["tags"] = project_tags
        parent.metadata["parent_id"] = parent_id

        # Store parent document
        parent_docs[parent_id] = parent

        # Split parent into children
        children = child_splitter.split_documents([parent])

        for child in children:
            # Add semantic tags to chunk content for better retrieval
            content_type = _detect_content_type(child.page_content)
            lang_tag = _detect_language_tag(child.page_content)

            # Prepend tags and breadcrumb to chunk content
            tagged_content = f"{content_type} {lang_tag} {project_tags} {breadcrumb}\n{child.page_content}"

            child.page_content = tagged_content
            child.metadata["parent_id"] = parent_id
            child.metadata["source"] = source
            child.metadata["breadcrumb"] = breadcrumb
            child.metadata["project_area"] = project_tags
            child.metadata["language"] = lang_tag.replace("[LANG=", "").replace("]", "")

            child_chunks.append(child)

    return child_chunks, parent_docs


def load_documents_with_parents(
    docs_dir: str,
    chunk_size: int,
    chunk_overlap: int,
) -> Tuple[List[Document], Dict[str, Document]]:
    """
    Load and chunk all documents from a directory.

    Returns:
        Tuple of (all_chunks, all_parent_docs)
    """
    all_chunks: List[Document] = []
    all_parents: Dict[str, Document] = {}

    if not os.path.exists(docs_dir):
        return all_chunks, all_parents

    for root, dirs, files in os.walk(docs_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.startswith('.') or not file.endswith('.md'):
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as handle:
                    content = handle.read()

                chunks, parents = chunk_document_with_parents(
                    content, file_path, chunk_size, chunk_overlap
                )
                all_chunks.extend(chunks)
                all_parents.update(parents)

            except Exception as exc:
                print(f"Skipping {file_path}: {exc}")

    return all_chunks, all_parents


# ============================================================
# Legacy functions for backward compatibility
# ============================================================

CODE_FENCE_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)\n```", re.DOTALL)
CODE_SIGNAL_RE = re.compile(
    r"\b(def|class|import|from|package|func|public|private|return|if|for|while)\b"
)
HEADER_RE = re.compile(r"(#{1,6} .+)")


def _is_navigation_chunk(text: str) -> bool:
    if "Skip to main content" not in text or "Navigation" not in text:
        return False
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    allowed = {"Skip to main content", "Navigation"}
    return all(line in allowed for line in lines)


def _code_density(code: str) -> float:
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    if not lines:
        return 0.0
    code_like = sum(1 for line in lines if CODE_SIGNAL_RE.search(line))
    return code_like / len(lines)


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def _make_text_chunks(
    text: str,
    source: str,
    chunks_list: List[Document],
    size: int,
    overlap: int,
) -> None:
    if len(text) <= size:
        chunks_list.append(Document(page_content=text, metadata={"source": source, "type": "text"}))
        return

    splits = HEADER_RE.split(text)
    sections = []
    i = 0
    while i < len(splits):
        if splits[i].startswith("#"):
            header = splits[i].strip()
            content = splits[i + 1] if i + 1 < len(splits) else ""
            sections.append(f"{header}\n{content}")
            i += 2
        else:
            if splits[i].strip():
                sections.append(splits[i])
            i += 1

    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(section) <= size:
            chunks_list.append(
                Document(page_content=section, metadata={"source": source, "type": "text"})
            )
            continue

        sentences = _split_sentences(section) or [section]
        current_chunk = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            if len(current_chunk) + len(sentence) + 1 <= size:
                current_chunk += sentence + " "
            else:
                chunk_text = current_chunk.strip()
                if chunk_text:
                    chunks_list.append(
                        Document(
                            page_content=chunk_text,
                            metadata={"source": source, "type": "text"},
                        )
                    )
                    overlap_words = chunk_text.split()[-max(overlap // 6, 5) :]
                    overlap_text = " ".join(overlap_words)
                    current_chunk = overlap_text + " " + sentence + " "
                else:
                    current_chunk = sentence + " "
        final_chunk = current_chunk.strip()
        if final_chunk:
            chunks_list.append(
                Document(page_content=final_chunk, metadata={"source": source, "type": "text"})
            )


def chunk_document(text: str, source: str, chunk_size: int, chunk_overlap: int) -> List[Document]:
    """Legacy chunking function for backward compatibility."""
    chunks: List[Document] = []
    cursor = 0

    for match in CODE_FENCE_RE.finditer(text):
        start, end = match.span()
        if start > cursor:
            pre_text = text[cursor:start]
            if pre_text.strip() and not _is_navigation_chunk(pre_text):
                cleaned = _strip_navigation_lines(pre_text)
                if cleaned.strip():
                    _make_text_chunks(cleaned, source, chunks, chunk_size, chunk_overlap)

        lang = (match.group(1) or "").strip()
        code = match.group(2)
        if code.strip():
            fence = f"```{lang}\n{code}\n```" if lang else f"```\n{code}\n```"
            density = _code_density(code)
            if density > 0.2:
                chunks.append(
                    Document(
                        page_content=fence,
                        metadata={
                            "source": source,
                            "type": "code",
                            "lang": lang,
                            "density": density,
                        },
                    )
                )
            else:
                _make_text_chunks(fence, source, chunks, chunk_size, chunk_overlap)

        cursor = end

    tail = text[cursor:]
    if tail.strip() and not _is_navigation_chunk(tail):
        cleaned = _strip_navigation_lines(tail)
        if cleaned.strip():
            _make_text_chunks(cleaned, source, chunks, chunk_size, chunk_overlap)

    return chunks


def load_documents(docs_dir: str, chunk_size: int, chunk_overlap: int) -> List[Document]:
    """Legacy document loading function for backward compatibility."""
    docs: List[Document] = []
    if not os.path.exists(docs_dir):
        return docs

    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.startswith("."):
                continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as handle:
                    content = handle.read()
                docs.extend(chunk_document(content, file_path, chunk_size, chunk_overlap))
            except Exception as exc:
                print(f"Skipping {file_path}: {exc}")
    return docs
