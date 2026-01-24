import os
import re
from typing import List

from langchain_core.documents import Document

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


def _strip_navigation_lines(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped in {"Skip to main content", "Navigation"}:
            continue
        lines.append(line)
    return "\n".join(lines)


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
