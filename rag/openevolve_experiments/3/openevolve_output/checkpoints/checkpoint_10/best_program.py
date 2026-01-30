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
        self.rerank_llm = None
        self.parent_docs = {} # storage for parent nodes
        
        # Hyperparameters for evolution
        self.chunk_size = 500 # Smaller chunks for better retrieval precision
        self.chunk_overlap = 100
        self.top_k_vector = 20 
        self.top_k_bm25 = 20
        self.weight_vector = 0.5
        self.weight_bm25 = 0.5
        self.rerank_top_n = 8 
        self.temperature = 0.0
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
        
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=self.temperature)
        self.rerank_llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
        
        # Ingestion
        all_chunks = []
        if os.path.exists(self.docs_dir):
            for root, dirs, files in os.walk(self.docs_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if not file.endswith('.md') or file.startswith('.'): continue
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text_content = f.read()
                        
                        # Apply evolved chunking strategy
                        chunks = self._chunk_document(text_content, file_path)
                        all_chunks.extend(chunks)
                    except Exception as e:
                        print(f"Skipping {file_path}: {e}")

        if not all_chunks:
            self.retriever = None
            return

        # Vector Retriever
        vector_db = FAISS.from_documents(all_chunks, embeddings)
        vector_retriever = vector_db.as_retriever(search_kwargs={"k": self.top_k_vector})
        
        # BM25 Retriever
        bm25_retriever = BM25Retriever.from_documents(all_chunks)
        bm25_retriever.k = self.top_k_bm25
        
        # Hybrid Ensemble (Base retrieval)
        ensemble_retriever = EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            weights=[self.weight_vector, self.weight_bm25]
        )
        self.retriever = ensemble_retriever
        
        gc.collect()

    def _flatten_markdown_tabs(self, text: str) -> str:
        """Unrolls Google-style tab widgets into sequential headers."""
        # Simple regex for {% tab label="Python" %} blocks
        pattern = r'{% tab label="(.*?)" %}(.*?){% endtab %}'
        def replacement(match):
            label = match.group(1)
            content = match.group(2)
            return f"\n\n#### {label} Implementation\n{content}\n"
        
        text = re.sub(r'{% tabs %}', '', text)
        text = re.sub(r'{% endtabs %}', '', text)
        return re.sub(pattern, replacement, text, flags=re.DOTALL)

    def _chunk_document(self, text: str, source: str) -> List[Any]:
        from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
        from langchain_core.documents import Document
        import uuid
        
        text = self._flatten_markdown_tabs(text)
        
        # 1. Split by headers to create Parent documents
        header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
            ("#", "h1"), ("##", "h2"), ("###", "h3"), ("####", "h4")
        ])
        parent_docs = header_splitter.split_text(text)
        
        child_chunks = []
        child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n```", "\n\n", "\n", " ", ""]
        )
        
        for p in parent_docs:
            parent_id = str(uuid.uuid4())
            breadcrumb = " > ".join([p.metadata.get(f"h{i}", "") for i in range(1, 5)]).strip(" > ")
            p.metadata["source"] = source
            p.metadata["breadcrumb"] = breadcrumb
            
            # Add language and project-area tags for better filtering and relevance
            lang_match = re.search(r'```(\w+)', p.page_content)
            language = lang_match.group(1).lower() if lang_match else "unknown"
            p.metadata["language"] = language
            
            # Heuristic project-area tagging based on breadcrumbs or source file path
            if re.search(r'a2a|auth', breadcrumb, re.I) or re.search(r'a2a|auth', source, re.I):
                p.metadata["project_area"] = "[A2A]"
            elif re.search(r'workflow', breadcrumb, re.I) or re.search(r'workflow', source, re.I):
                p.metadata["project_area"] = "[WORKFLOW]"
            else:
                p.metadata["project_area"] = "[GENERAL]"
                
            self.parent_docs[parent_id] = p
            
            # 2. Split parents into children
            for c in child_splitter.split_documents([p]):
                # Add tagging for better semantic separation
                prefix = "[DOC_CODE]" if "```" in c.page_content else "[DOC_TEXT]"
                c.page_content = f"{prefix} {breadcrumb} {p.metadata['project_area']}\n{c.page_content}"
                c.metadata["parent_id"] = parent_id
                c.metadata["source"] = source
                c.metadata["language"] = language
                c.metadata["project_area"] = p.metadata["project_area"]
                child_chunks.append(c)
                
        return child_chunks

    def _llm_rerank(self, query: str, docs: List[Any]) -> List[Any]:
        """Rerank candidates using a small LLM with enhanced prompt for language, completeness, and snippet type detection."""
        if not docs: return []
        
        packed = []
        # Detect requested language from query for reranker prompt emphasis
        requested_lang = None
        lang_match = re.search(r'\b(python|go|java)\b', query, re.I)
        if lang_match:
            requested_lang = lang_match.group(1).lower()
        
        for i, d in enumerate(docs):
            # Heuristic completeness detection for full API defs vs partial snippet
            snippet = d.page_content[:1400].replace('\n', ' ').strip()
            completeness_tag = "[COMPLETE_API]" if re.search(r'\b(class|func|def)\s+\w+', snippet, re.I) else "[PARTIAL]"
            
            # Mark language if available and if matches requested language
            lang_tag = d.metadata.get("language", "unknown")
            lang_flag = "[LANG_MATCH]" if requested_lang and lang_tag == requested_lang else "[LANG_OTHER]"
            
            meta = d.metadata.get("breadcrumb", "") + " " + d.metadata.get("source", "")
            packed.append(f"[{i}] {completeness_tag} {lang_flag} Metadata: {meta}\nContent: {snippet}")
        
        prompt = (
            "Role: ADK Expert Reranker.\n"
            "Goal: Assign a relevance score (0-100) to each chunk for the user query.\n"
            "Prioritize:\n"
            "- Chunks containing complete API definitions or well-formed code examples.\n"
            "- Chunks with exact API names matching the query.\n"
            "- Chunks in the user's requested programming language if specified (Python, Go, Java).\n"
            "- Penalize partial snippets and chunks in other languages.\n"
            f"User Query: {query}\n\n"
            "Chunks:\n" + "\n\n".join(packed) + "\n\n"
            "Return JSON with 'scores' mapping chunk_id to score (0-100)."
        )
        
        try:
            import json
            res = self.rerank_llm.invoke(prompt)
            # Use regex to find JSON if model adds fluff
            match = re.search(r'\{.*\}', res.content, re.DOTALL)
            if not match: return docs[:self.rerank_top_n]
            
            scores = json.loads(match.group(0)).get("scores", {})
            # Rank indices by score
            ranked_indices = sorted(range(len(docs)), 
                                    key=lambda i: float(scores.get(str(i), scores.get(i, 0))), 
                                    reverse=True)
            return [docs[i] for i in ranked_indices[:self.rerank_top_n]]
        except Exception as e:
            print(f"Reranking failed: {e}")
            return docs[:self.rerank_top_n]

    def query(self, query_str: str) -> Dict[str, Any]:
        if not self.retriever:
            return {"answer": "No documents ingested.", "contexts": []}

        # 1. Retrieval (Hybrid)
        candidates = self.retriever.invoke(query_str)
        
        # 2. Cross-language filtering: detect requested language from query and filter candidates
        requested_lang = None
        lang_pattern = re.compile(r'\b(python|go|java)\b', re.I)
        lang_match = lang_pattern.search(query_str)
        if lang_match:
            requested_lang = lang_match.group(1).lower()
        
        if requested_lang:
            candidates = [c for c in candidates if c.metadata.get("language", "") == requested_lang]
            # If filtered too strictly, fallback to original set
            if len(candidates) < 3:
                candidates = self.retriever.invoke(query_str)
        
        # 3. Reranking
        top_chunks = self._llm_rerank(query_str, candidates)
        
        # 4. Parent Retrieval & Formatting
        final_contexts = []
        seen_parents = set()
        context_block = ""
        
        # Summarize parent context titles for brevity and clarity
        for c in top_chunks:
            p_id = c.metadata.get("parent_id")
            if p_id in self.parent_docs and p_id not in seen_parents:
                parent = self.parent_docs[p_id]
                seen_parents.add(p_id)
                final_contexts.append(parent.page_content)
                src = os.path.basename(parent.metadata.get("source", "unknown"))
                breadcrumb = parent.metadata.get("breadcrumb", "")
                # Use XML style tags for clarity and better chunk separation
                context_block += (
                    f"<source file='{src}' section='{breadcrumb}'>\n"
                    f"{parent.page_content}\n"
                    f"</source>\n\n"
                )

        # 5. Generation (Strict Grounding)
        prompt = (
            "You are a technical expert on Google ADK. Answer the user's question STRICTLY using the provided context. "
            "Follow these rules:\n"
            "1. If the answer is not in the context, explicitly state 'I don't know from the provided documentation'.\n"
            "2. When mentioning API classes or methods, use the EXACT names found in the context.\n"
            "3. Use the 'Quote then Explain' pattern: first quote the relevant doc/code, then provide your explanation.\n"
            "4. If multiple languages are available (Python, Go, Java), only provide the one requested by the user. If none requested, default to Python but mention others exist.\n"
            "5. Clearly indicate the programming language of any code snippet you quote.\n\n"
            f"Context:\n{context_block}\n\n"
            f"Question: {query_str}\n\n"
            "Answer:"
        )
        
        res = self.llm.invoke(prompt)
        gc.collect()
        
        return {"answer": res.content, "contexts": final_contexts}
# EVOLVE-BLOCK-END
