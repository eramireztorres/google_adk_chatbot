import os
import re
import gc
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
# Imports removed from top-level to prevent parent process initialization
# They are now lazy-loaded in RAGSystem.__init__ to ensure fork-safety

class RAGSystem:
    def __init__(self, docs_dir: str):
        self.docs_dir = docs_dir
        self.retriever = None
        self.llm = None
        
        # Hyperparameters for evolution
        self.chunk_size = 1200 # Increased for better context
        self.chunk_overlap = 250
        self.top_k_vector = 15 # High k for retrieval phase
        self.top_k_bm25 = 10
        self.weight_vector = 0.6 # Preference for semantic
        self.weight_bm25 = 0.4
        self.rerank_top_n = 5 # Strict reranking for generation
        self.temperature = 0.1
        self.expand_query = False 
        
        # Load env from multiple possible locations
        env_paths = [
            os.path.join(os.path.dirname(__file__), '.env'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        ]
        for p in env_paths:
            if os.path.exists(p):
                load_dotenv(p)
                
        self._initialize_system()

    def _initialize_system(self):
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from langchain_core.documents import Document
        from langchain_community.vectorstores import FAISS
        from langchain_community.retrievers import BM25Retriever
        from langchain_classic.retrievers import EnsembleRetriever
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Ingestion
        documents = []
        if os.path.exists(self.docs_dir):
            for root, dirs, files in os.walk(self.docs_dir):
                # Efficiently skip hidden directories (in-place)
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.startswith('.'): continue
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text_content = f.read()
                        
                        # Apply evolved chunking strategy
                        chunks = self._chunk_document(text_content, file_path)
                        documents.extend(chunks)
                    except Exception as e:
                        print(f"Skipping {file_path}: {e}")

        if not documents:
            self.retriever = None
            return

        # Vector Retriever
        vector_db = FAISS.from_documents(documents, embeddings)
        vector_retriever = vector_db.as_retriever(search_kwargs={"k": self.top_k_vector})
        
        # BM25 Retriever
        bm25_retriever = BM25Retriever.from_documents(documents)
        bm25_retriever.k = self.top_k_bm25
        
        # Hybrid Ensemble (Base retrieval)
        ensemble_retriever = EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            weights=[self.weight_vector, self.weight_bm25]
        )
        self.retriever = ensemble_retriever

        # Generation Config
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=self.temperature)
        
        # Immediate cleanup of temporary ingestion objects
        gc.collect()

    def _chunk_document(self, text: str, source: str) -> List[Any]:
        # Lazy import for safety
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document
        
        # 2-stage chunking with header path metadata for context-aware splitting
        # First, split by top-level markdown headers (to isolate sections)
        header_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size * 3,
            chunk_overlap=0,
            separators=["\n# ", "\n## ", "\n### ", "\n#### "]
        )
        header_sections = header_splitter.create_documents([text], metadatas=[{"source": source}])
        
        # Then chunk each section into smaller chunks with overlap and add header_path metadata
        small_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        all_chunks = []
        for section_doc in header_sections:
            # Extract header path from the start lines of the section content
            lines = section_doc.page_content.splitlines()
            header_path = ""
            for line in lines:
                if line.strip().startswith("#"):
                    header_path = line.strip()
                    break
            content_start = 0
            if header_path:
                try:
                    content_start = lines.index(header_path) + 1
                except Exception:
                    content_start = 0
            content_text = "\n".join(lines[content_start:]) if content_start < len(lines) else section_doc.page_content

            # Chunk the content smaller with header_path metadata
            chunks = small_splitter.create_documents([content_text], metadatas=[{"source": source, "header_path": header_path}])
            all_chunks.extend(chunks)
        
        return all_chunks

    def _expand_query_logic(self, query: str) -> str:
        if not self.expand_query:
            return query
        
        prompt = f"Provide 2-3 different ways to ask the following question to improve search recall:\nQuestion: {query}\nOutput ONLY the expanded queries, one per line."
        res = self.llm.invoke(prompt)
        expansions = res.content.split('\n')
        return query + " " + " ".join(expansions[:2])

    def query(self, query_str: str) -> Dict[str, Any]:
        if not self.retriever:
            return {"answer": "No documents ingested.", "contexts": []}

        # Retrieval
        search_query = self._expand_query_logic(query_str)
        docs = self.retriever.invoke(search_query)
        
        # --- AD-HOC RERANKING ---
        # Rerank retrieved docs by boosting those with header_path containing "Reference" or "API"
        def rerank_key(doc):
            header_path = doc.metadata.get("header_path", "").lower()
            score = 0
            if "reference" in header_path:
                score += 2
            if "api" in header_path:
                score += 1.5
            # Also boost longer chunks moderately (up to 1 point)
            score += min(len(doc.page_content) / 1000.0, 1.0)
            return score

        docs = sorted(docs, key=rerank_key, reverse=True)
        
        # Limit to top rerank_top_n docs for prompt context to reduce noise
        limited_docs = docs[:self.rerank_top_n]
        
        contexts = [d.page_content for d in limited_docs]
        sources = [d.metadata.get("source", "unknown") for d in limited_docs]
        
        context_block = ""
        for i, (content, src) in enumerate(zip(contexts, sources)):
            header_path = limited_docs[i].metadata.get("header_path", "")
            header_info = f" [{header_path}]" if header_path else ""
            context_block += f"Source {i+1} ({os.path.basename(src)}){header_info}:\n{content}\n\n"

        # Generation prompt with chain-of-thought and mandatory terms analysis
        prompt = (
            f"Question: {query_str}\n\n"
            f"Context:\n{context_block}\n\n"
            "Step 1: Identify any mandatory terms, definitions, or key concepts related to the question in the context.\n"
            "Step 2: Based strictly on the context, provide a detailed answer. "
            "If code examples are present, prioritize them in your explanation. "
            "Include relevant detail while staying faithful. "
            "If the answer is not found, say 'I don't know'."
        )
        
        res = self.llm.invoke(prompt)
        
        # Cleanup
        gc.collect()
        
        return {"answer": res.content, "contexts": contexts}
# EVOLVE-BLOCK-END
