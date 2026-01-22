import os
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# --- BOILERPLATE: DO NOT EVOLVE ---
_rag_system_cache = None

def evaluate_rag(docs_path: str, query: str) -> Dict[str, Any]:
    global _rag_system_cache
    try:
        # Simple caching to avoid re-ingesting for every query if docs path hasn't changed
        if _rag_system_cache is None or _rag_system_cache.docs_dir != docs_path:
            _rag_system_cache = RAGSystem(docs_path)
            
        return _rag_system_cache.query(query)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"answer": f"Error: {str(e)}", "contexts": []}
# --- END BOILERPLATE ---

# EVOLVE-BLOCK-START
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

class RAGSystem:
    def __init__(self, docs_dir: str):
        self.docs_dir = docs_dir
        self.vector_store = None
        self.llm = None
        
        # Hyperparameters for evolution
        self.chunk_size = 1000              # Increase chunk size for richer context per chunk
        self.chunk_overlap = 250            # Increase overlap to preserve context continuity
        self.top_k = 8                      # Slightly higher top_k for more context coverage
        self.temperature = 0.2              # Lower temperature for more precise answers
        
        # Load env
        load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
        self._initialize_system()

    def _initialize_system(self):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Ingestion
        docs = []
        if os.path.exists(self.docs_dir):
            for root, _, files in os.walk(self.docs_dir):
                for file in files:
                    if file.startswith('.'): continue
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text_content = f.read()
                        
                        # Apply evolved chunking strategy
                        chunks = self._chunk_document(text_content, file_path)
                        docs.extend(chunks)
                    except Exception as e:
                        print(f"Skipping {file_path}: {e}")

        # Vector Store (FAISS)
        if docs:
            self.vector_store = FAISS.from_documents(docs, embeddings)
            # Normalize vectors for cosine similarity to improve retrieval quality
            try:
                import faiss
                # Ensure index uses cosine similarity by normalizing vectors internally
                # We must normalize vectors ourselves before adding to index (FAISS expects this)
                from numpy import linalg, asarray
                def normalize(vectors):
                    norms = linalg.norm(vectors, axis=1, keepdims=True)
                    return vectors / (norms + 1e-10)
                # Extract embeddings matrix and normalize
                xb = self.vector_store.index.reconstruct_n(0, self.vector_store.index.ntotal)
                xb_norm = normalize(xb)
                # Rebuild index with normalized vectors
                self.vector_store.index.reset()
                self.vector_store.index = faiss.IndexFlatIP(embeddings.embedding_dimension)
                self.vector_store.index.add(xb_norm)
            except Exception:
                pass
        else:
            self.vector_store = None

        # Generation Config
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=self.temperature)

    def _chunk_document(self, text: str, source: str) -> List[Document]:
        """
        Ad-hoc chunking logic adapted from run_ingestion.py.
        """
        # Regex patterns from run_ingestion.py
        CODE_FENCE_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)\n```", re.DOTALL)
        CODE_SIGNAL_RE = re.compile(r"\b(def|class|import|from|package|func|public|private|return|if|for|while)\b")
        
        def _is_navigation_chunk(txt: str) -> bool:
            return "Skip to main content" in txt and "Navigation" in txt
            
        def _code_density(txt: str) -> float:
            lines = [line.strip() for line in txt.splitlines() if line.strip()]
            if not lines: return 0.0
            code_like = sum(1 for line in lines if CODE_SIGNAL_RE.search(line))
            return code_like / len(lines)

        chunks = []
        cursor = 0
        
        # Split by code fences first
        for match in CODE_FENCE_RE.finditer(text):
            start, end = match.span()
            if start > cursor:
                pre_text = text[cursor:start]
                if pre_text.strip():
                    if not _is_navigation_chunk(pre_text):
                        self._make_text_chunks(pre_text, source, chunks, self.chunk_size, self.chunk_overlap)
            
            lang = (match.group(1) or "").strip()
            code = match.group(2)
            
            # Logic to keep code blocks atomic
            if code.strip():
                fence = f"```{lang}\n{code}\n```"
                density = _code_density(code)
                # If high density or explicitly fenced, treat as code
                if density > 0.2:
                     chunks.append(Document(
                         page_content=fence, 
                         metadata={"source": source, "type": "code", "lang": lang, "density": density}
                     ))
                else:
                    # Treat as text if low density code
                    self._make_text_chunks(fence, source, chunks, self.chunk_size, self.chunk_overlap)
            
            cursor = end
            
        tail = text[cursor:]
        if tail.strip() and not _is_navigation_chunk(tail):
            self._make_text_chunks(tail, source, chunks, self.chunk_size, self.chunk_overlap)
            
        return chunks

    def _make_text_chunks(self, text: str, source: str, chunks_list: List[Document], size: int, overlap: int):
        # Improved chunking: split on markdown headers and respect sentence boundaries for semantic coherence
        HEADER_RE = re.compile(r"(#{1,6} .+)")
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        from nltk.tokenize import sent_tokenize

        # If text small enough, no splitting
        if len(text) <= size:
            chunks_list.append(Document(page_content=text, metadata={"source": source, "type": "text"}))
            return
        
        # Split on headers if possible
        splits = HEADER_RE.split(text)
        # splits alternate between non-header and header lines
        sections = []
        i = 0
        while i < len(splits):
            if splits[i].startswith('#'):
                header = splits[i].strip()
                content = splits[i+1] if i+1 < len(splits) else ''
                sections.append(header + "\n" + content)
                i += 2
            else:
                # Text before first header or in between headers
                if splits[i].strip():
                    sections.append(splits[i])
                i += 1
        
        # Now chunk sections further using sentence tokenization if needed
        for sec in sections:
            sec = sec.strip()
            if len(sec) <= size:
                chunks_list.append(Document(page_content=sec, metadata={"source": source, "type": "text"}))
            else:
                sentences = sent_tokenize(sec)
                current_chunk = ""
                for idx, sentence in enumerate(sentences):
                    if len(current_chunk) + len(sentence) + 1 <= size:
                        current_chunk += sentence + " "
                    else:
                        chunks_list.append(Document(page_content=current_chunk.strip(), metadata={"source": source, "type": "text"}))
                        # Overlap: reuse last ~overlap/6 words from previous chunk but try to not break sentences abruptly
                        overlap_words = current_chunk.strip().split()[-max(overlap//6,5):]
                        # Try to extend overlap to full sentences (simple heuristic: include sentences that fit)
                        overlap_text = " ".join(overlap_words)
                        current_chunk = overlap_text + " " + sentence + " "
                if current_chunk.strip():
                    chunks_list.append(Document(page_content=current_chunk.strip(), metadata={"source": source, "type": "text"}))

    def query(self, query_str: str) -> Dict[str, Any]:
        if not self.vector_store:
            return {"answer": "No documents ingested.", "contexts": []}

        # Retrieval: use MMR for more diverse relevant results if available
        try:
            retrieved = self.vector_store.max_marginal_relevance_search(query_str, k=self.top_k, fetch_k=10)
        except AttributeError:
            # fallback to similarity search if MMR not supported
            retrieved = self.vector_store.similarity_search(query_str, k=self.top_k)
        
        contexts = [d.page_content for d in retrieved]
        sources = [d.metadata.get("source", "unknown") for d in retrieved]
        
        context_block = ""
        for i, (content, src) in enumerate(zip(contexts, sources)):
            context_block += f"Source {i+1} ({src}):\n{content}\n\n"

        # Generation
        prompt = (
            f"You are an expert assistant for Google ADK documentation.\n"
            f"Question: {query_str}\n\n"
            f"Context:\n{context_block}\n\n"
            "Answer the question based strictly on the context provided. "
            "If the context contains code examples, use them to illustrate your answer. "
            "Be concise, accurate, and faithful to the context. "
            "If you cannot answer from the context, say 'I don't know based on the provided context.'"
        )
        
        res = self.llm.invoke(prompt)
        return {"answer": res.content, "contexts": contexts}
# EVOLVE-BLOCK-END
