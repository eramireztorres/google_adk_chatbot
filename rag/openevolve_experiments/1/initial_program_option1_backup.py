import os

# --- THREAD PINNING: FORK SAFETY ---
# Must be set BEFORE any library imports (numpy, torch, faiss)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

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
        # --- LAZY IMPORTS FOR FORK SAFETY ---
        # Moving these imports inside the method ensures they are loaded
        # ONLY in the worker process, avoiding broken thread pools from fork()
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from langchain_core.documents import Document
        from langchain_community.vectorstores import FAISS
        from langchain_community.retrievers import BM25Retriever
        from langchain_classic.retrievers import EnsembleRetriever, ContextualCompressionRetriever
        from langchain_community.document_compressors import FlashrankRerank
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

        # Reranking Layer (Wrapped in safety net for stability)
        try:
            compressor = FlashrankRerank(top_n=self.rerank_top_n)
            self.retriever = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=ensemble_retriever
            )
        except Exception as e:
            print(f"Warning: FlashrankRerank failed to initialize, falling back to base ensemble: {e}")
            self.retriever = ensemble_retriever

        # Generation Config
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=self.temperature)
        
        # Immediate cleanup of temporary ingestion objects
        gc.collect()

    def _chunk_document(self, text: str, source: str) -> List[Any]:
        # Lazy import for safety
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document
        
        # Advanced separators to honor markdown hierarchy
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n# ", "\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""]
        )
        return splitter.create_documents([text], metadatas=[{"source": source}])

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

        # Retrieval + Reranking (Auto-handled by ContextualCompressionRetriever)
        search_query = self._expand_query_logic(query_str)
        docs = self.retriever.invoke(search_query)
        
        contexts = [d.page_content for d in docs]
        sources = [d.metadata.get("source", "unknown") for d in docs]
        
        context_block = ""
        for i, (content, src) in enumerate(zip(contexts, sources)):
            context_block += f"Source {i+1} ({os.path.basename(src)}):\n{content}\n\n"

        # Generation
        prompt = (
            f"Question: {query_str}\n\n"
            f"Context:\n{context_block}\n\n"
            "Answer the question based strictly on the context provided. "
            "If the context contains code examples, prioritize them in your answer. "
            "Include as much relevant detail as possible while staying faithful. "
            "If the answer is not in the context, say you don't know."
        )
        
        res = self.llm.invoke(prompt)
        
        # Cleanup
        gc.collect()
        
        return {"answer": res.content, "contexts": contexts}
# EVOLVE-BLOCK-END
