
import os
import sys
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

if not os.getenv("OPENAI_API_KEY"):
    print("CRITICAL ERROR: OPENAI_API_KEY is NOT set.")
else:
    k = os.getenv("OPENAI_API_KEY")
    print(f"OPENAI_API_KEY found: {k[:8]}...{k[-4:]}")

from src.adk_chatbot.knowledge_base import get_knowledge_base

CODE_FENCE_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)\n```", re.DOTALL)
CODE_SIGNAL_RE = re.compile(
    r"\b(def|class|import|from|package|func|public|private|return|if|for|while)\b"
)
PY_SIGNAL_RE = re.compile(r"\b(def|class|import|from)\b")
JAVA_SIGNAL_RE = re.compile(r"\b(import java\.|public class|private class|class )\b")
GO_SIGNAL_RE = re.compile(r"\b(package|func|import \\(|go )\b")

def _is_navigation_chunk(text: str) -> bool:
    return "Skip to main content" in text and "Navigation" in text

def _split_markdown(text: str):
    chunks = []
    cursor = 0
    for match in CODE_FENCE_RE.finditer(text):
        start, end = match.span()
        if start > cursor:
            pre = text[cursor:start]
            if pre.strip():
                chunks.append({"kind": "text", "text": pre})
        lang = (match.group(1) or "").strip()
        code = match.group(2)
        if code.strip():
            fence = f"```{lang}\n{code}\n```" if lang else f"```\n{code}\n```"
            chunks.append({"kind": "code", "text": fence, "lang": lang})
        cursor = end

    tail = text[cursor:]
    if tail.strip():
        chunks.append({"kind": "text", "text": tail})
    return chunks

def _infer_code_lang(code: str, fence_lang: str | None) -> str | None:
    if fence_lang:
        return fence_lang.lower()
    sample = code.strip()
    if sample.startswith("package ") or "google.golang.org" in code:
        return "go"
    if "import com." in code or "public class" in code:
        return "java"
    if "def " in code or "from " in code or "import " in code:
        return "python"
    return None

def _is_code_like(code: str) -> bool:
    return bool(CODE_SIGNAL_RE.search(code))

def _code_density(code: str) -> float:
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    if not lines:
        return 0.0
    code_like = sum(1 for line in lines if CODE_SIGNAL_RE.search(line))
    return code_like / len(lines)

def _detect_languages(code: str) -> List[str]:
    py_hits = len(PY_SIGNAL_RE.findall(code))
    java_hits = len(JAVA_SIGNAL_RE.findall(code))
    go_hits = len(GO_SIGNAL_RE.findall(code))
    langs = []
    if py_hits >= 2:
        langs.append("python")
    if java_hits >= 2:
        langs.append("java")
    if go_hits >= 2:
        langs.append("go")
    return langs

def main():
    print("Initializing RAG Ingestion...")
    
    # Path to documentation - configurable if needed
    docs_path = "/home/erick/repo/adk_chatbot/docs/adk_docs"
    
    if not os.path.exists(docs_path):
        print(f"Error: Docs directory not found at {docs_path}")
        return

    try:
        # Get Knowledge Base directly (No Agent/LLM init required for ingestion)
        knowledge = get_knowledge_base()
        
        print(f"--- Starting ingestion from {docs_path} ---")
        files_processed = 0
        
        for root, _, files in os.walk(docs_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Skip hidden files
                if file.startswith('.'):
                    continue
                    
                try:
                    # Assuming text/markdown files
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                        chunks = _split_markdown(text_content)
                        chunk_index = 0
                        for chunk in chunks:
                            if chunk["kind"] == "text" and _is_navigation_chunk(chunk["text"]):
                                continue
                            content_kind = chunk["kind"]
                            code_lang = None
                            density = None
                            if chunk["kind"] == "code":
                                density = _code_density(chunk["text"])
                                if not _is_code_like(chunk["text"]) or density < 0.2:
                                    content_kind = "text"
                                code_lang = _infer_code_lang(chunk["text"], chunk.get("lang"))
                                lang_hits = _detect_languages(chunk["text"])
                                if len(lang_hits) > 1:
                                    code_lang = "mixed"
                            metadata = {
                                "source_path": file_path,
                                "doc_type": "doc",
                                "content_kind": content_kind,
                            }
                            if code_lang:
                                metadata["code_lang"] = code_lang
                            if density is not None and content_kind == "code":
                                metadata["code_density"] = density
                            name = f"{file_path}#chunk{chunk_index}"
                            knowledge.add_content(
                                text_content=chunk["text"],
                                name=name,
                                metadata=metadata,
                            )
                            chunk_index += 1
                        files_processed += 1
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")
        
        print(f"--- Ingested {files_processed} files. ---")
        print("Ingestion Complete.")
        
    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    main()
