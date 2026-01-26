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
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAGSystem:
    def __init__(self, docs_dir: str):
        self.docs_dir = docs_dir
        self.retriever = None
        self.llm = None
        
        # Hyperparameters for evolution
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.top_k_vector = 4
        self.top_k_bm25 = 4
        self.weight_vector = 0.5
        self.weight_bm25 = 0.5
        self.temperature = 0.2
        self.expand_query = False # Potential for evolution
        
        # Load env
        load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
        self._initialize_system()

    def _initialize_system(self):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Ingestion
        documents = []
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
        
        # Hybrid Ensemble
        self.retriever = EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            weights=[self.weight_vector, self.weight_bm25]
        )

        # Generation Config
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=self.temperature)

    def _chunk_document(self, text: str, source: str) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n## ", "\n### ", "\n#### ", "\n", " ", ""]
        )
        return splitter.create_documents([text], metadatas=[{"source": source}])

    def _expand_query_logic(self, query: str) -> str:
        # Placeholder for query expansion evolution
        if not self.expand_query:
            return query
        
        # Simple expansion prompt
        prompt = f"Provide 2-3 different ways to ask the following question to improve search recall:\nQuestion: {query}\nOutput ONLY the expanded queries, one per line."
        res = self.llm.invoke(prompt)
        # Use first expansion + original for retrieval (simplified for now)
        expansions = res.content.split('\n')
        return query + " " + " ".join(expansions[:2])

    def query(self, query_str: str) -> Dict[str, Any]:
        if not self.retriever:
            return {"answer": "No documents ingested.", "contexts": []}

        # Retrieval
        search_query = self._expand_query_logic(query_str)
        docs = self.retriever.invoke(search_query)
        
        contexts = [d.page_content for d in docs]
        sources = [d.metadata.get("source", "unknown") for d in docs]
        
        context_block = ""
        for i, (content, src) in enumerate(zip(contexts, sources)):
            context_block += f"Source {i+1} ({src}):\n{content}\n\n"

        # Generation
        prompt = (
            f"Question: {query_str}\n\n"
            f"Context:\n{context_block}\n\n"
            "Answer the question based strictly on the context provided. "
            "If the context contains code examples, prioritize them in your answer. "
            "If the answer is not in the context, say you don't know."
        )
        
        res = self.llm.invoke(prompt)
        return {"answer": res.content, "contexts": contexts}
# EVOLVE-BLOCK-END
