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
        """Unrolls Google-style tab widgets into sequential headers with normalized language tags."""
        # Enhanced regex for {% tab label="Python" %} blocks with language normalization
        pattern = r'{% tab label="(.*?)" %}(.*?){% endtab %}'
        def replacement(match):
            label = match.group(1).strip()
            content = match.group(2)
            lang_map = {"py": "Python", "python": "Python", "go": "Go", "golang": "Go", "java": "Java"}
            lang_tag = lang_map.get(label.lower(), label)
            # Append a standardized language tag for chunk tagging synergy
            return f"\n\n#### [{lang_tag}] {label} Implementation\n{content}\n"
        
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
            
            # Add project-area tags if identifiable from breadcrumb (example)
            project_tags = []
            if re.search(r'\[A2A\]', breadcrumb): project_tags.append("[A2A]")
            if re.search(r'\[WORKFLOW\]', breadcrumb): project_tags.append("[WORKFLOW]")
            if project_tags:
                p.metadata["tags"] = " ".join(project_tags)
            else:
                p.metadata["tags"] = ""
            
            self.parent_docs[parent_id] = p
            
            # 2. Split parents into children
            for c in child_splitter.split_documents([p]):
                # Add tagging for better semantic separation
                prefix = "[DOC_CODE]" if "```" in c.page_content else "[DOC_TEXT]"
                # Detect language from code fences for tagging
                lang_tag = ""
                lang_match = re.search(r'```(\w+)', c.page_content)
                if lang_match:
                    lang = lang_match.group(1).lower()
                    if lang in ("python", "go", "java"):
                        lang_tag = f"[LANG={lang.capitalize()}]"
                    else:
                        lang_tag = "[LANG=Unknown]"
                else:
                    lang_tag = "[LANG=Unknown]"
                # Add tags and breadcrumb into chunk content for better reranking and generation
                # Also add project area tag into chunk content for reranker synergy
                project_area = p.metadata.get("tags", "[GENERAL]")
                c.page_content = f"{prefix} {lang_tag} {project_area} {breadcrumb}\n{c.page_content}"
                c.metadata["parent_id"] = parent_id
                c.metadata["source"] = source
                c.metadata["project_area"] = project_area
                child_chunks.append(c)
                
        return child_chunks

    def _llm_rerank(self, query: str, docs: List[Any]) -> List[Any]:
        """Rerank candidates using a small LLM with enhanced prompt for multi-language & completeness detection."""
        if not docs: return []
        
        packed = []
        requested_lang = None
        # Detect requested language from query for prompt emphasis
        lang_match = re.search(r'\b(python|go|java)\b', query, re.I)
        if lang_match:
            requested_lang = lang_match.group(1).lower()

        for i, d in enumerate(docs):
            snippet = d.page_content[:1400].replace('\n', ' ').strip()
            completeness_tag = "[COMPLETE_API]" if re.search(r'\b(class|func|def|interface|type|package|func\s+main)\s+\w*', snippet, re.I) else "[PARTIAL]"
            lang = d.metadata.get("language", "unknown").lower()
            requested_lang_tag = "[REQUESTED_LANG]" if requested_lang and lang == requested_lang else ""
            tags = d.metadata.get("tags", "")
            breadcrumb = d.metadata.get("breadcrumb", "")
            packed.append(f"[{i}] {completeness_tag} {requested_lang_tag} Tags:{tags} Breadcrumb:{breadcrumb}\n{snippet}")

        prompt = (
            "Role: ADK Expert Reranker.\n"
            "Goal: Score each chunk from 0 to 100 for relevance to the query.\n"
            "Prioritize chunks with:\n"
            "- Exact API names matching the query\n"
            "- Complete API definitions over partial snippets\n"
            "- Code examples in the user's requested programming language\n"
            "- Proper handling of multi-language snippets\n"
            f"User Query: {query}\n\n"
            "Chunks:\n" + "\n\n".join(packed) + "\n\n"
            "Return JSON object with 'scores' mapping chunk IDs to numeric scores."
        )

        try:
            import json
            res = self.rerank_llm.invoke(prompt)
            match = re.search(r'\{.*\}', res.content, re.DOTALL)
            if not match:
                return docs[:self.rerank_top_n]

            scores = json.loads(match.group(0)).get("scores", {})
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
        
        # Detect requested language from query (simple heuristic)
        requested_lang = None
        lang_candidates = ["python", "go", "java"]
        lower_query = query_str.lower()
        for lang in lang_candidates:
            if lang in lower_query:
                requested_lang = lang.capitalize()
                break
        if not requested_lang:
            requested_lang = "Python"  # default
        
        # 2. Cross-language filtering: filter candidates to requested language if specified
        filtered_candidates = []
        for c in candidates:
            # Use chunk language tag in content or fallback to unknown
            lang_tag_search = re.search(r'\[LANG=(\w+)\]', c.page_content)
            chunk_lang = lang_tag_search.group(1) if lang_tag_search else "Unknown"
            # Include chunks with unknown language for Python requests to avoid losing recall
            if requested_lang == "Python" and chunk_lang in ("Python", "Unknown"):
                filtered_candidates.append(c)
            elif chunk_lang == requested_lang:
                filtered_candidates.append(c)
        # Use filtered candidates only if enough remain, else fallback to full candidate set
        if filtered_candidates and len(filtered_candidates) >= max(3, self.rerank_top_n):
            candidates = filtered_candidates
        else:
            # If too few, fallback to original for recall preservation
            pass
        
        # 3. Reranking
        top_chunks = self._llm_rerank(query_str, candidates)
        
        # 4. Parent Retrieval & Formatting
        final_contexts = []
        seen_parents = set()
        context_block = ""
        
        for c in top_chunks:
            p_id = c.metadata.get("parent_id")
            if p_id in self.parent_docs and p_id not in seen_parents:
                parent = self.parent_docs[p_id]
                # Filter parent context by language tag similarly
                lang_tag_search = re.search(r'\[LANG=(\w+)\]', parent.page_content)
                parent_lang = lang_tag_search.group(1) if lang_tag_search else "Unknown"
                # Accept unknown language parents for Python queries to preserve recall
                if requested_lang == "Python" and parent_lang not in ("Python", "Unknown"):
                    continue
                elif requested_lang != "Python" and parent_lang != requested_lang:
                    continue
                
                seen_parents.add(p_id)
                final_contexts.append(parent.page_content)
                src = os.path.basename(parent.metadata.get("source", "unknown"))
                breadcrumb = parent.metadata.get("breadcrumb", "")
                # Wrap each source in XML-style tags for clearer separation
                context_block += f"<source file=\"{src}\" section=\"{breadcrumb}\">\n{parent.page_content}\n</source>\n\n"

        # 5. Generation (Strict Grounding)
        prompt = (
            "You are a technical expert on Google ADK. Answer the user's question STRICTLY using the provided context. "
            "Follow these rules:\n"
            "1. If the answer is not in the context, explicitly state 'I don't know from the provided documentation'.\n"
            "2. When mentioning API classes or methods, use the EXACT names found in the context.\n"
            "3. Use the 'Quote then Explain' pattern: first quote the relevant doc/code, then provide your explanation.\n"
            f"4. Only provide code or examples in the requested language: {requested_lang}. "
            "If none requested, default to Python but mention other languages exist.\n\n"
            "5. Clearly indicate the programming language of any code snippet you quote.\n\n"
            "6. Use XML tags to indicate sources.\n"
            f"Context:\n{context_block}\n\n"
            f"Question: {query_str}\n\n"
            "Answer:"
        )
        
        # Use caching for llm.invoke to reduce latency on repeated queries (optional)
        res = self.llm.invoke(prompt)
        gc.collect()
        
        return {"answer": res.content, "contexts": final_contexts}
# EVOLVE-BLOCK-END
