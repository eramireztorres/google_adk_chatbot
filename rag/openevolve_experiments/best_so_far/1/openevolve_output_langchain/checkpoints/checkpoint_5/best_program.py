import os
import time
from typing import Dict, Any

# --- BOILERPLATE: DO NOT EVOLVE ---
_rag_system_cache = None

def evaluate_rag(docs_path: str, query: str) -> Dict[str, Any]:
    global _rag_system_cache
    try:
        if _rag_system_cache is None or _rag_system_cache.docs_dir != docs_path:
            _rag_system_cache = RAGSystem(docs_path)
        return _rag_system_cache.query(query)
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "contexts": []}
# --- END BOILERPLATE ---

# EVOLVE-BLOCK-START
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

class RAGSystem:
    def __init__(self, docs_dir: str):
        self.docs_dir = docs_dir
        self.vector_store = None
        self.llm = None
        self._initialized = False
        self._initialize_system()

    def _initialize_system(self):
        if self._initialized:
            return

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        try:
            probe_vec = embeddings.embed_query("probe")
            if not probe_vec or len(probe_vec) == 0:
                raise ValueError("embedding probe returned empty vector")
        except Exception as e:
            raise RuntimeError(f"embedding_probe_failed: {e}")

        loader = DirectoryLoader(
            self.docs_dir,
            glob="**/*.md",
            loader_cls=TextLoader,
            recursive=True,
            silent_errors=True,
        )
        docs = loader.load()
        splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=200)
        splits = splitter.split_documents(docs)

        self.vector_store = InMemoryVectorStore(embeddings)
        self.vector_store.add_documents(splits)

        self.llm = ChatOpenAI(model="gpt-4.1-mini")
        self._initialized = True

    def query(self, query_str: str) -> Dict[str, Any]:
        retrieved = self.vector_store.similarity_search(query_str, k=3)
        context = "\n\n---\n\n".join(d.page_content for d in retrieved)
        prompt = (
            "You are an expert assistant. Use the following extracted context to answer the question.\n\n"
            f"EXTRACTED CONTEXT:\n{context}\n\nQUESTION:\n{query_str}\n"
            "If the answer cannot be found in the context, reply that you do not know.\n"
        )
        answer = self.llm.invoke(prompt).content.strip()
        contexts = [d.page_content for d in retrieved]
        return {"answer": answer, "contexts": contexts}
# EVOLVE-BLOCK-END
