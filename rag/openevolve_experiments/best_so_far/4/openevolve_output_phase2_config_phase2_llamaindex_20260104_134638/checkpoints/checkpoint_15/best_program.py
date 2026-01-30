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
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.postprocessor import LLMRerank
from llama_index.core.query_engine import RetrieverQueryEngine

class RAGSystem:
    def __init__(self, docs_dir: str):
        self.docs_dir = docs_dir
        self.index = None
        self.query_engine = None
        self._initialized = False
        self._initialize_system()

    def _initialize_system(self):
        if self._initialized:
            return
        Settings.llm = OpenAI(model="gpt-4.1-mini", temperature=0.0)
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
        # Increase chunk size and overlap for semantic splitting
        Settings.chunk_size = 512
        Settings.chunk_overlap = 128

        try:
            probe_vec = Settings.embed_model.get_text_embedding("probe")
            if not probe_vec or len(probe_vec) == 0:
                raise ValueError("embedding probe returned empty vector")
        except Exception as e:
            raise RuntimeError(f"embedding_probe_failed: {e}")

        reader = SimpleDirectoryReader(
            input_dir=self.docs_dir,
            recursive=True,
            required_exts=[".md", ".txt"],
        )
        documents = reader.load_data()
        try:
            splitter = SemanticSplitterNodeParser()
            nodes = splitter.get_nodes_from_documents(documents)
        except Exception:
            # Fallback to SentenceSplitter with larger chunk size and overlap
            from llama_index.core.node_parser import SentenceSplitter
            splitter = SentenceSplitter(chunk_size=512, chunk_overlap=128)
            nodes = splitter.get_nodes_from_documents(documents)

        self.index = VectorStoreIndex(nodes)
        retriever = self.index.as_retriever(similarity_top_k=5)
        reranker = LLMRerank(top_n=3)
        self.query_engine = RetrieverQueryEngine(
            retriever,
            node_postprocessors=[reranker],
        )
        self._initialized = True

    def query(self, query_str: str) -> Dict[str, Any]:
        response = self.query_engine.query(query_str)
        contexts = [node.node.get_content() for node in response.source_nodes]
        return {"answer": str(response), "contexts": contexts}
# EVOLVE-BLOCK-END
