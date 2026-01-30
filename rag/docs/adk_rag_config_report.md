# RAG for Google ADK Docs (Mixed Markdown + Multi‑Language Code)
**Date:** 2026-01-29  
**Goal:** Accurate Q&A over Google ADK docs you downloaded as Markdown, with *minimal code hallucinations*, using **OpenAI** models, and keeping it **fast**.

This report focuses on **chunking**, **embeddings**, **retrieval**, **reranking**, and **anti-hallucination** tactics that work well when docs mix:
- prose + API reference
- code blocks in **Python / Java / Go**
- CLI snippets, config blocks, and short “how-to” fragments

Sources used (requested):  
- Qodo: “RAG for a Codebase with 10k Repos” citeturn1view0  
- Qodo: “Evaluating RAG for large scale codebases” citeturn1view1  
- Qodo: “What Is RAG and Why Does It Matter for Code Quality?” citeturn3view0  
- Reddit r/Rag thread on API refs citeturn1view2  
Plus some supporting context on reranking and “advanced RAG” methods. citeturn0search10turn0search30

---

## 1) What makes ADK docs hard for RAG?
**Mixed modalities within Markdown**:
- A single page may include conceptual prose + code examples for multiple SDKs.
- “Answerable” information often lives in *small code snippets* (imports, method names) where missing context causes hallucinations.

**Failure modes**:
1. **Chunk boundary damage**: code gets split mid‑function or separated from required imports / class definitions.
2. **“Lost in the middle”**: retrieval returns many chunks; the most relevant is not in the prompt or is buried.
3. **Semantic-only retrieval misses exact APIs**: token-level exact matches (class/method names) matter a lot.

Qodo explicitly notes that incomplete/invalid code chunks can *increase hallucinations* and that chunking must keep critical context (imports, class defs) with retrieved units. citeturn1view0

---

## 2) Recommended architecture (fast + accurate)
Use a **two-stage retrieval pipeline**:

### Stage A — Candidate retrieval (cheap)
- **Hybrid search**: BM25 (lexical) + vector similarity
- Pull **top_k = 20–40** candidates (fast)
- Apply **MMR** or diversification to avoid near-duplicate chunks

### Stage B — Rerank (precision)
- Rerank the candidates with either:
  - a dedicated reranker (cross-encoder), *or*
  - a fast LLM rerank (OpenAI mini model)
- Keep **top_n = 6–10** chunks to feed the generator.

This directly targets the “lost in the middle” issue and improves relevance. citeturn0search10turn0search30

---

## 3) Chunking strategies that work for mixed Markdown + code

### 3.1 The “Section-first + code-aware” splitter (best default)
**Rule:** chunk by Markdown structure first, then refine with code boundaries.

**Steps:**
1. Split by headers (`#`, `##`, `###`) to keep topics coherent.
2. Within each section:
   - Preserve **code fences** (```...```) as atomic units when possible.
   - If a code fence is large, split **inside** the code using language-aware rules (AST/CST when possible; otherwise safe heuristics).
3. Create chunks that are **small**, but include **critical context**.

Qodo describes keeping related context (imports + class definitions) together with method chunks to avoid incomplete code retrieval. citeturn1view0

**Target sizes (good starting point):**
- prose-only chunks: **300–800 tokens**
- code-centric chunks: **150–400 tokens**
- overlap: **~10–15%** (or overlap by section context rather than raw characters)

### 3.2 “Parent/Child” chunking (excellent for Q&A)
Store:
- **Parent** = the full section (e.g., `## Tools for Agents`), 1–3k tokens
- **Child** = smaller fragments (paragraphs, code blocks)

Retrieve children, but when answering, attach the parent context *selectively* (e.g., include the header path + 1–2 adjacent paragraphs).

This boosts factual grounding while staying compact.

### 3.3 Special handling for code blocks
For each code fence:
- Detect language from the fence: ```python, ```java, ```go, ```ts
- Add metadata: `code_lang=python|java|go|ts`, `is_code=true`, `path`, `heading_path`
- If code references symbols not in the code block (imports, earlier definitions), consider **context stitching**:
  - attach the nearest preceding import snippet / setup snippet within the same section

This mirrors Qodo’s “retroactive processing” idea: re-add critical context that got separated by splitting. citeturn1view0

---

## 4) Embeddings (OpenAI) for mixed text+code
### Recommended embedding model
- **text-embedding-3-large** for maximum retrieval quality
- **text-embedding-3-small** if you need cheaper/faster with acceptable quality

For docs with lots of exact API identifiers, embeddings alone can miss exact matches — that’s why hybrid search is important.

### Add metadata and “content type tags”
A practical trick: prefix each chunk with a lightweight tag before embedding:

- For prose chunk:
  ```
  [DOC_TEXT] heading_path=... file=... 
  <content>
  ```
- For code chunk:
  ```
  [DOC_CODE lang=python] heading_path=... file=...
  <code fence content>
  ```

This often improves semantic separation without needing separate indexes.

---

## 5) Retrieval strategies (ranked)
### 5.1 Hybrid retrieval (vector + BM25) — **strongly recommended**
Why: API Q&A often depends on exact strings (class/method names), where BM25 shines.

Implementation options:
- **LangChain**: use a vector store + BM25 retriever and combine with an ensemble.
- **LlamaIndex**: use hybrid retriever if your backend supports it, or implement a custom fusion retriever.

### 5.2 MMR (diversified top-k)
Use MMR to avoid retrieving 8 near-duplicate chunks from the same page. This helps when docs repeat the same snippet in multiple places.

### 5.3 Query rewriting / multi-query (optional)
For user questions like:
> “How do I store files between sessions in ADK?”

You can generate 2–5 alternative queries (“Artifacts”, “MemoryService”, “session state”, …) and merge retrieval results.
This improves recall but costs extra latency.

### 5.4 “Section routing” (fast, high impact)
If you have ADK docs organized into folders/sections (e.g., `agents/`, `tools/`, `sessions/`, `tutorials/`), do a quick classifier/rule:
- If query contains “tool”, “function tool”, “register” → boost `tools/` pages.
- If query contains “memory”, “session” → boost `sessions/`.

This is cheap and often improves first-pass retrieval.

---

## 6) Reranking (high leverage for correctness)
Reranking is where many “expert” pipelines get their lift.

### Option A — Cross-encoder reranker (fast + strong relevance)
Examples (open-source):
- `bge-reranker-large` or similar cross-encoders

Pros: strong ranking; Cons: extra infra.

### Option B — LLM reranker (OpenAI mini model)
Use a small OpenAI model to score candidates with a constrained rubric:
- “Does this chunk contain the exact API/class/method requested?”
- “Does it include a usage example?”
- “Is it a conceptual explanation?”

Keep outputs structured (JSON scores) and pick top_n.

This aligns with the general “multiple phases” view of RAG pipelines (retrieval + rerank + generation). citeturn1view1

---

## 7) Anti-hallucination tactics for code Q&A
These are the highest ROI changes for “accurate Q&A avoiding code hallucinations”.

### 7.1 Strict grounding prompt (must)
In the answer prompt:
- require citing the retrieved chunks
- require *verbatim* copying of API names from context
- allow “I don’t know from the docs” if not present

### 7.2 “Quote then explain” pattern
For API questions:
1. Quote the relevant doc lines / code block
2. Explain what it means
3. Provide a minimal example (only using what was quoted)

### 7.3 Symbol verification guard (post-check)
Before returning an answer that contains code:
- extract identifiers (e.g., `ArtifactService`, `MemoryService`, method names)
- verify they appear in retrieved context
- if not, either:
  - remove/soften claims, or
  - retrieve again with the missing symbols as queries

This simple check catches a lot of hallucinated method names.

---

## 8) Concrete: LangChain pipeline (Markdown folder)
Below is a **reference implementation** you can adapt to your folder of Markdown files.

> Notes:
> - This example uses a vector store + BM25 hybrid + rerank compression.
> - You can swap the vector store (FAISS, Chroma, Qdrant).
> - Reranking shown as an LLM-based reranker for simplicity.

```python
import os
from typing import List, Dict, Any

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document

# 1) Load Markdown files
loader = DirectoryLoader(
    "./adk-docs-md",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)
docs = loader.load()

# 2) Split by Markdown headers first
header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")])

section_docs: List[Document] = []
for d in docs:
    for sd in header_splitter.split_text(d.page_content):
        # Preserve original file metadata
        sd.metadata.update(d.metadata)
        section_docs.append(sd)

# 3) Refine: recursive splitter inside each section (keeps code fences reasonably intact)
#    You can improve this by writing a code-fence-aware splitter (recommended).
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,     # tune based on tokenization
    chunk_overlap=150,
    separators=["\n```", "\n\n", "\n", " ", ""],
)

chunks: List[Document] = []
for sd in section_docs:
    for c in text_splitter.split_documents([sd]):
        # Add "heading_path" convenience metadata
        heading_path = " > ".join([sd.metadata.get("h1",""), sd.metadata.get("h2",""), sd.metadata.get("h3","")]).strip(" >")
        c.metadata["heading_path"] = heading_path
        chunks.append(c)

# 4) Build vector index
emb = OpenAIEmbeddings(model="text-embedding-3-large")
vs = FAISS.from_documents(chunks, emb)

# 5) Build BM25 retriever (lexical)
bm25 = BM25Retriever.from_documents(chunks)
bm25.k = 20

# 6) Hybrid ensemble retriever
vec_retriever = vs.as_retriever(search_kwargs={"k": 20})
hybrid = EnsembleRetriever(
    retrievers=[bm25, vec_retriever],
    weights=[0.45, 0.55],
)

# 7) Optional: LLM rerank (fast rubric)
rerank_llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

RERANK_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are reranking retrieved documentation chunks for answering a user question about Google ADK. "
     "Return JSON with a relevance score 0-100 for each chunk id. Prefer chunks that contain exact API names, "
     "function signatures, or code examples directly answering the question."),
    ("user",
     "Question:\n{question}\n\nChunks:\n{chunks}\n\nReturn JSON: {{'scores': {{chunk_id: score, ...}}}}")
])

def llm_rerank(question: str, docs: List[Document], top_n: int = 8) -> List[Document]:
    packed = []
    for i, d in enumerate(docs):
        packed.append(f"[{i}] file={d.metadata.get('source','')} heading={d.metadata.get('heading_path','')}\n{d.page_content[:1200]}")
    msg = RERANK_PROMPT.format_messages(question=question, chunks="\n\n".join(packed))
    raw = rerank_llm.invoke(msg).content

    # naive parse; replace with robust json parse in production
    import json, re
    m = re.search(r"\{.*\}", raw, re.S)
    scores = json.loads(m.group(0))["scores"] if m else {}
    ranked = sorted(range(len(docs)), key=lambda i: scores.get(str(i), scores.get(i, 0)), reverse=True)
    return [docs[i] for i in ranked[:top_n]]

# 8) QA prompt (strict grounding)
qa_llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You answer questions about Google ADK ONLY using the provided context. "
     "If the answer is not in the context, say you don't know from the docs. "
     "When you mention an API/class/method, it must appear verbatim in the context. "
     "Prefer quoting relevant lines/code blocks, then explaining."),
    ("user", "Question:\n{question}\n\nContext:\n{context}")
])

def answer(question: str) -> str:
    candidates = hybrid.get_relevant_documents(question)
    top = llm_rerank(question, candidates, top_n=8)
    context = "\n\n---\n\n".join([f"FILE: {d.metadata.get('source','')}\nHEADING: {d.metadata.get('heading_path','')}\n{d.page_content}" for d in top])
    return qa_llm.invoke(QA_PROMPT.format_messages(question=question, context=context)).content

print(answer("How do I use tools in ADK agents?"))
```

**Key improvements you can add next**:
- A real code-fence-aware / language-aware splitter
- Symbol verification guard before returning code
- Caching rerank results for repeated queries

---

## 9) Concrete: LlamaIndex pipeline (Markdown folder)
LlamaIndex is strong for “document structure + retrieval + response synthesis”.

### Recommended pattern
- Use a Markdown parser / node parser that respects headers
- Add metadata (file path, header path, code_lang)
- Use a vector index + optional hybrid retrieval
- Add a reranker / postprocessor

```python
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

# 1) Read markdown files
reader = SimpleDirectoryReader(
    input_dir="./adk-docs-md",
    recursive=True,
    required_exts=[".md"],
)
documents = reader.load_data()

# 2) Markdown-aware parsing (keeps header structure)
parser = MarkdownNodeParser()
nodes = parser.get_nodes_from_documents(documents)

# 3) Embed + index
embed_model = OpenAIEmbedding(model="text-embedding-3-large")
index = VectorStoreIndex(nodes, embed_model=embed_model)

# 4) Query engine with compact context + low temperature
llm = OpenAI(model="gpt-4.1-mini", temperature=0)
query_engine = index.as_query_engine(
    llm=llm,
    similarity_top_k=12,    # later rerank down
)

resp = query_engine.query("Explain how ADK artifacts work and where they are stored.")
print(resp)
```

To add reranking in LlamaIndex, use a **node postprocessor** (cross-encoder reranker or LLM reranker) and then shrink to `top_n`.

---

## 10) Practical “best defaults” for your use case (fast & grounded)

### Ingestion defaults (start here)
- Split by headers first
- Chunk size: ~800–1200 tokens, overlap ~100–200 tokens
- Preserve code fences
- Attach metadata: `source`, `heading_path`, `is_code`, `code_lang`

### Retrieval defaults
- Hybrid retrieval, `top_k=20` each
- MMR diversification
- Rerank to `top_n=6–10`

### Generation defaults
- Model: `gpt-4.1-mini`, `temperature=0`
- Strict grounding prompt + “quote then explain”
- Output includes file+heading citations

---

## 11) Evaluation (so you know it’s working)
Qodo recommends focusing evaluation on:
- **retrieval accuracy** (did we fetch the right chunks?)
- **answer correctness** (end-to-end)
and emphasizes using robust evaluation loops (ground-truth datasets + LLM-as-judge or human review). citeturn1view1

For your project:
- Create 30–100 QA pairs you personally care about (ADK tools, artifacts, memory, sessions, agents)
- Track:
  - hit rate for “correct chunk in top_n”
  - exactness of API names
  - hallucinated identifiers count

---

## 12) Notes from the Reddit thread (API reference RAG)
The thread you linked frames the common problem: models struggle on lesser-known APIs and RAG helps, but **retrieval quality & code-aware embeddings/reranking matter**. citeturn1view2  
A key practical takeaway: if your retrieval doesn’t surface the exact “right” snippet, generation will degrade quickly — so prioritize hybrid retrieval + reranking.

---

## 13) If you do only 3 things, do these
1. **Section-first + code-aware chunking** (avoid broken code; keep imports/defs with examples). citeturn1view0  
2. **Hybrid retrieval (BM25 + vector)** for API identifiers.  
3. **Rerank to a small context** (6–10 chunks), then use a **strict grounding prompt**.

---

### Appendix: Useful ADK doc entry points
(These are good “anchors” to ensure your corpus includes core concepts.)
- ADK “Tools” page citeturn0search16  
- ADK “Artifacts” page citeturn0search9  
- ADK “Memory” page citeturn0search20  
- ADK tutorials index citeturn0search12  

---

**End.**
