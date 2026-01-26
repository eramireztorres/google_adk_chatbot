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
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.top_k = 5
        self.temperature = 0.7
        
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
        # Standard rolling window split for text parts
        if len(text) <= size:
            chunks_list.append(Document(page_content=text, metadata={"source": source, "type": "text"}))
            return
            
        start = 0
        while start < len(text):
            end = min(start + size, len(text))
            chunk_text = text[start:end]
            chunks_list.append(Document(page_content=chunk_text, metadata={"source": source, "type": "text"}))
            start += size - overlap
            if start >= len(text): break

    def query(self, query_str: str) -> Dict[str, Any]:
        if not self.vector_store:
            return {"answer": "No documents ingested.", "contexts": []}

        # Retrieval
        retrieved = self.vector_store.similarity_search(query_str, k=self.top_k)
        contexts = [d.page_content for d in retrieved]
        sources = [d.metadata.get("source", "unknown") for d in retrieved]
        
        context_block = ""
        for i, (content, src) in enumerate(zip(contexts, sources)):
            context_block += f"Source {i+1} ({src}):\n{content}\n\n"

        # Generation
        prompt = (
            f"Question: {query_str}\n\n"
            f"Context:\n{context_block}\n\n"
            "Answer the question based strictly on the context provided. "
            "If the context contains code examples, prioritize them in your answer."
        )
        
        res = self.llm.invoke(prompt)
        return {"answer": res.content, "contexts": contexts}
# EVOLVE-BLOCK-END
