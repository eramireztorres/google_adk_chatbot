# Architectural Analysis and Implementation Strategy for Retrieval-Augmented Generation on Google Agent Development Kit (AdK) Documentation

## Executive Summary

The implementation of Retrieval-Augmented Generation (RAG) pipelines for
technical documentation---specifically software development kits (SDKs)
like the Google Agent Development Kit (AdK)---presents a distinct class
of engineering challenges that differ fundamentally from standard prose
retrieval. Technical documentation is a composite data structure
characterized by high information density, non-linear reading paths, and
the interleaving of natural language explanations with syntactically
rigid code blocks. When this content is distributed across multiple
programming languages (Python, Java, Go), the complexity of semantic
retrieval multiplies significantly.

This report provides an exhaustive technical analysis and implementation
guide for constructing a high-performance RAG system tailored to the
Google AdK documentation. It relies on a \"Small-to-Big\" retrieval
paradigm, advocating for hierarchical indexing strategies that decouple
the retrieval unit (granular chunks) from the generation unit (broad
context). The analysis evaluates and recommends specific configurations
for chunking (Markdown-aware and Abstract Syntax Tree parsing),
embedding (code-specialized models like voyage-code-2), and retrieval
(hybrid keyword/vector search with Cross-Encoder reranking).

Furthermore, this document addresses the specific \"mixed-modality\"
problem where Python, Java, and Go examples coexist. It proposes a
Metadata-First Indexing strategy where language tags are treated as hard
filters or weighted vector components, ensuring that a user query for a
Python implementation does not retrieve hallucinated Java syntax. The
report concludes with concrete, production-ready code implementations
using both the LlamaIndex and LangChain frameworks, demonstrating how to
parse Google-style Markdown, handle tabbed code widgets, and deploy a
recursive retrieval architecture.

## 1. Domain Analysis: The Morphology of Technical Documentation

To design an effective pipeline, one must first deconstruct the anatomy
of the source data. The Google AdK documentation, downloaded as Markdown
files, is not merely a collection of text files; it is a structured
knowledge graph flattened into a file system. Unlike linear prose (e.g.,
novels or news articles), technical documentation exhibits unique
structural and semantic characteristics that defeat \"naive\" RAG
implementations.

### 1.1 The Mixed-Modality Challenge

Standard RAG pipelines treat data as homogenous text. However, technical
documentation contains two distinct modalities that require conflicting
processing strategies:

1.  **Explanatory Prose (Natural Language):** This text explains *why*
    > and *how* a concept works. It relies on semantic meaning,
    > synonyms, and narrative flow. It is best retrieved using dense
    > vector embeddings which capture semantic similarity (e.g.,
    > \"authentication\" \$\\approx\$ \"login\").

2.  **Code Snippets (Formal Language):** This text demonstrates
    > implementation. It relies on exact syntax, variable names, and
    > import paths. It is highly sensitive to whitespace and structure.
    > It is often best retrieved using sparse keyword search (BM25) or
    > specialized code embeddings, as generic semantic models may
    > confuse visually similar but functionally distinct code (e.g., a
    > GET request vs. a POST request).^1^

When these two modalities are interleaved in a single Markdown file,
standard fixed-size chunking (e.g., \"split every 512 tokens\") leads to
catastrophic context fracture. A chunk might start in the middle of a
Python function and end in the middle of a Java class, stripping both of
their necessary headers and import statements. This necessitates a
chunking strategy that respects the boundaries of both Markdown headers
and code blocks.^2^

### 1.2 The \"Tabbed\" Code Widget Problem

A specific characteristic of modern documentation, including Google\'s,
is the use of UI tabs to display code examples for multiple languages
(Python, Java, Go) for a single operation. In the rendered HTML, these
appear as clickable tabs. However, in the raw Markdown source, this
often appears in one of two forms:

-   **Sequential Fenced Blocks:** The code blocks appear one after
    > another, separated only by a minor text label or a specific
    > Markdown widget syntax.

-   **HTML/Liquid Widgets:** The use of specific tags like {% tab %} or
    > HTML \<div\> structures.^3^

**Implication for RAG:** If a naive chunking strategy processes this
sequentially, a query for \"How to initialize agent in Python\" might
retrieve a chunk containing the Java code because it appears immediately
adjacent to the Python code and shares the same descriptive text. The
system must be engineered to treat these as *parallel* siblings rather
than *sequential* text. If the retrieval window slides over the Java
code to capture the context for the Python code, it introduces \"noise
tokens\" that can cause the LLM to hallucinate syntax from the wrong
language.^1^

### 1.3 Contextual Dependency and Header Hierarchy

Technical docs are deeply hierarchical. A paragraph describing a list()
method is meaningless without knowing it belongs to the Conversation
class, which belongs to the Memory module. Flattening this hierarchy
into isolated chunks results in \"orphan chunks\"---text that has no
standalone meaning. For example, a chunk reading *\"Arguments:
retention_period (int): Days to keep messages\"* is useless to an LLM
unless it knows *which function* accepts this argument.

Therefore, the pipeline must implement **Parent Document Retrieval** or
**Metadata Enrichment**, where every chunk inherits the breadcrumbs of
its document structure (e.g., Module: Memory \> Class: Conversation \>
Method: list).^5^

## 2. Strategic Data Preprocessing and Ingestion

The \"Garbage In, Garbage Out\" principle is the primary failure mode
for RAG applications. For the Google AdK documentation, we require a
sophisticated ingestion pipeline that parses structure before embedding.

### 2.1 Parsing Strategy: Markdown-Specific vs. Text-Generic

Generic text loaders (like standard Python open().read()) are
insufficient. We must use parsers that understand the Abstract Syntax
Tree (AST) of Markdown. The goal is to transform the flat file into a
tree of nodes.

**Recommended Approach:** Use **LlamaIndex MarkdownNodeParser** or
**LangChain MarkdownHeaderTextSplitter**.

These parsers split text based on Markdown headers (\#, \#\#, \#\#\#).

-   **Input:** A 50-page guide on \"Agent Configuration\".

-   **Output:** Hierarchical nodes corresponding to sections.

-   **Metadata Injection:** The parser must be configured to cascade
    > header information down to the leaf nodes. A snippet of code
    > inside a section \#\# Authentication \> \#\#\# OAuth must carry
    > the metadata {\'section\': \'Authentication\', \'subsection\':
    > \'OAuth\'}.^5^

### 2.2 The \"Tab Unrolling\" Technique

To address the tabbed code issue described in 1.2, we should apply \"Tab
Unrolling\" during preprocessing. This involves a pre-ingestion script
that detects the widget syntax and restructures the document.

**Tab Unrolling Algorithm:**

1.  **Detection:** Scan the Markdown AST for sequences of code blocks
    > that are grouped by widget tags (e.g., {% tab label=\"Python\"
    > %}).

2.  **Duplication:** Identify the *preceding* explanatory paragraph (the
    > \"anchor\" text).

3.  **Expansion:** Create distinct, synthesized sections for each
    > language.

    -   Synthesize a header: \#\#\# Python Implementation.

    -   Insert the anchor text.

    -   Insert the Python code block.

    -   Repeat for Java and Go.

4.  **Replacement:** Replace the original widget block with these
    > sequential, explicitly labeled sections.

This ensures that regardless of which language the user asks about, the
retrieved chunk contains both the explanation and the correct code
snippet, without the noise of the other languages.^4^

### 2.3 Language Tagging and Filtering

We must implement a **Language-Specific Routing/Filtering** strategy at
the ingestion stage. We cannot rely on the LLM to filter languages
during generation; it wastes context window tokens and increases
hallucination risk.

**Algorithm for Code Block Processing:**

1.  **Identification:** Scan the Markdown AST for fenced code blocks.

2.  **Tagging:** Extract the language identifier (e.g., py, java, go).
    > If missing, use a classifier like magika ^7^ or guesslang to infer
    > the language.

3.  **Separation:**

    -   **Option A (Split Indices):** Create separate vector indices for
        > adk_python, adk_java, and adk_go. This guarantees zero
        > contamination but increases infrastructure complexity.

    -   **Option B (Metadata Filtering - Recommended):** Ingest all
        > chunks into a single vector store but attach a hard metadata
        > filter language=\[\'python\'\], language=\[\'java\'\], or
        > language=\[\'text\'\]. Text chunks describing concepts are
        > tagged language=\[\'all\'\] or language=\[\'text\'\].

## 3. Advanced Chunking Strategies

Selecting the correct chunking strategy is the single most significant
factor in RAG performance for coding tasks.

### 3.1 Limitations of Fixed-Size Chunking

Standard \"sliding window\" chunking (e.g., 512 tokens with 50 overlap)
is detrimental for code.

-   **Logic Breaking:** It splits function definitions from their
    > bodies, or decorators from the functions they modify.

-   **Syntactic Invalidity:** It creates chunks with open braces { or
    > parentheses ( that are never closed, confusing the embedding model
    > which expects syntactically valid constructs.

### 3.2 Strategy 1: Hierarchical Markdown Splitting (The Backbone)

This strategy aligns chunks with the logical structure of the document.

-   **Level 1 (Parent):** The full section under a generic header (e.g.,
    > \#\# Context Management). This might be 2,000 tokens. It holds the
    > complete semantic context.

-   **Level 2 (Child):** Paragraphs and code blocks within that section.
    > These are 200-500 tokens.

**Mechanism:** We index the **Child** chunks for retrieval (vectors are
generated for children). However, when a child is retrieved, we return
the **Parent** chunk to the LLM. This is known as \"Small-to-Big\"
retrieval.^8^

-   *Why it works:* A user query \"how to set context\" matches the
    > specific sentence in the child chunk. But the answer requires the
    > full code example and explanation found in the parent chunk.

### 3.3 Strategy 2: Code-Aware Splitting (AST-Based)

For the code blocks themselves, we must use AST-based splitters.

-   **Python:** Uses ast module or tree-sitter. Splits on class and def
    > boundaries.

-   **Java/Go:** Uses tree-sitter.

**Configuration for Google AdK:**

Since AdK documentation is likely explanatory (Markdown) containing
Code, we should prioritize **Markdown Splitting** as the primary method,
and apply **Code Splitting** only *inside* the large code blocks found
within the Markdown.

**Recommended Configuration:**

-   **Text Splitter:** MarkdownHeaderTextSplitter (LangChain) or
    > MarkdownNodeParser (LlamaIndex).

-   **Code Splitter:** Recursive character splitter using separators
    > tailored for code: \[\"\\nclass \", \"\\ndef \", \"\\nfunc \",
    > \"\\n\\n\", \"\\n\", \" \"\].^9^

  **Feature**              **Fixed-Size Chunking**   **Semantic Chunking**   **Hierarchical (Small-to-Big)**
  ------------------------ ------------------------- ----------------------- ---------------------------------
  **Logic Preservation**   Low                       High                    **Very High**
  **Context Window**       Efficient                 Variable                **Optimized**
  **Implementation**       Simple                    Moderate                **Complex**
  **Code Suitability**     Poor                      Good                    **Excellent**

### 3.4 Token Limits and Overlap

-   **Embedding Model Limit:** If using text-embedding-3-large (8191
    > tokens), we have flexibility. If using older models (512 tokens),
    > we must be strict.

-   **Recommendation:**

    -   **Retrieval Chunks:** 512 tokens. (Large enough to capture a
        > full function signature and docstring, small enough to be
        > semantically precise).

    -   **Overlap:** 150 tokens. (Higher overlap is needed for code to
        > capture surrounding context like imports or class variables).

## 4. Semantic Representation: Embedding Models

The choice of embedding model dictates the system\'s ability to
understand that adk.Agent() is semantically related to \"create a new
bot instance\".

### 4.1 The \"Code-Text Gap\"

Standard NLP models (like BERT or early Ada) are trained on prose. They
struggle to associate natural language queries (\"how to connect to
Spanner\") with code implementation (spanner_client = spanner.Client()).
The vector space for \"connect\" might be far from Client().

### 4.2 Recommended Models

Based on current benchmarks ^10^, the following models are recommended
for mixed text/code:

1.  **Voyage AI (voyage-code-2):**

    -   **Architecture:** Optimized specifically for code retrieval
        > tasks.

    -   **Pros:** Superior performance in mapping natural language to
        > code; large context window (16k tokens); specialized in
        > identifying code function despite variable naming.^13^

    -   **Cons:** Proprietary API; usage costs.

    -   **Verdict:** **Primary Recommendation** for high-performance AdK
        > RAG.

2.  **OpenAI (text-embedding-3-large):**

    -   **Architecture:** General-purpose dense retrieval.

    -   **Pros:** Strong performance on MTEB leaderboards; handles mixed
        > modalities adequately; native support in almost all tools;
        > flexible dimensionality.^14^

    -   **Cons:** Generic, not code-specialized; may miss subtle
        > syntactic nuances.

    -   **Verdict:** Excellent fallback and easier to implement.

3.  **BAAI (bge-m3 or bge-en-icl):**

    -   **Architecture:** Open-source dense retrieval.

    -   **Pros:** State-of-the-art dense retrieval; supports
        > multi-granularity; free to run if infrastructure permits.

    -   **Cons:** Requires GPU infrastructure for low latency.

### 4.3 Hybrid Search (Sparse + Dense)

For SDK documentation, **Hybrid Search is non-negotiable**.

-   **Scenario:** User searches for a specific error code ADK_ERR_004 or
    > a specific method plan_execute.

-   **Vector Search Failure:** Semantic models might map ADK_ERR_004 to
    > \"generic error\" or \"bug\". It might miss the exact alphanumeric
    > match.

-   **Keyword Search (BM25) Success:** BM25 will find the exact document
    > containing ADK_ERR_004.

**Architecture:**

-   **Vector Store:** Weaviate, Qdrant, or Pinecone (Serverless). All
    > support Hybrid search.^15^

-   **Configuration:** Weighting alpha (\$\\alpha\$). \$\\alpha=1.0\$ is
    > pure vector, \$\\alpha=0.0\$ is pure keyword.

-   **Recommendation:** \$\\alpha=0.7\$ (Favor semantic, but keep strong
    > keyword influence) for documentation queries.

## 5. Retrieval and Reranking Architecture

Retrieving the top-k chunks is only the first step. The raw retrieval
often contains noise---outdated API versions, irrelevant languages, or
tangentially related concepts.

### 5.1 Two-Stage Retrieval Process

#### Stage 1: Broad Retrieval (Recall)

-   Fetch top 50 candidates using Hybrid Search.

-   Apply Metadata Filters: language IN \[user_query_language,
    > \'text\'\].

#### Stage 2: Reranking (Precision)

-   Use a **Cross-Encoder** model to score the relevance of the 50
    > candidates against the query.

-   Cross-encoders process the query and document *simultaneously*,
    > allowing them to detect subtle nuances (like identifying that a
    > chunk is about *deprecating* a feature, not *using* it) that
    > vector distances miss.

**Recommended Rerankers:**

-   **Cohere Rerank (rerank-english-v3.0):** Industry standard,
    > extremely effective for code.

-   **BAAI/bge-reranker-large:** Excellent open-source alternative.^16^

### 5.2 Recursive / Parent Document Retrieval

As introduced in Section 3.2, this is the architectural \"secret sauce\"
for documentation RAG.

1.  **Index:** Small chunks (Child nodes).

2.  **Retrieve:** Small chunks based on vector similarity.

3.  **Resolve:** Look up the Parent Node ID associated with the
    > retrieved Child.

4.  **Return:** The Parent Node (Full Section text) to the LLM.

This solves the \"Missing Context\" problem. The LLM sees the whole
method definition, headers, and warnings, even if the vector match was
only on a single line of code.^6^

### 5.3 Query Understanding and Expansion (HyDE)

Users often ask imprecise questions: *\"How do I make the agent talk?\"*

The documentation might use terms like *\"Conversational Interface\"* or
*\"Response Generation\"*.

**HyDE (Hypothetical Document Embeddings):**

1.  LLM generates a *hypothetical* code snippet or documentation
    > paragraph answering the user\'s query.

    -   *User:* \"How to connect to database?\"

    -   *HyDE:* \"To connect to the database in Google AdK, use the
        > DatabaseClient class with credentials\...\"

2.  Embed this hypothetical answer.

3.  Retrieve real documents similar to the hypothetical answer.

*Note:* For code, HyDE can be risky if the model hallucinates a
non-existent API. **Query Decomposition** is often safer: Break a
complex question (\"How to build a RAG agent with Spanner?\") into
sub-questions (\"How to initialize Agent\", \"How to use Spanner
tool\").^17^

## 6. Implementation Guide: LlamaIndex Pipeline

This implementation focuses on the \"Small-to-Big\" strategy using
LlamaIndex\'s native node parsing and recursive retrieval capabilities.

### 6.1 Custom Ingestion with Language Filtering

Python

import os\
from llama_index.core import SimpleDirectoryReader, Document\
from llama_index.core.node_parser import MarkdownNodeParser,
RecursiveCharacterTextSplitter\
from llama_index.core.schema import IndexNode\
from llama_index.embeddings.openai import OpenAIEmbedding\
from llama_index.core import VectorStoreIndex, StorageContext\
from llama_index.vector_stores.chroma import ChromaVectorStore\
import chromadb\
\
\# Initialize embedding model (Switch to Voyage if available)\
embed_model = OpenAIEmbedding(model=\"text-embedding-3-large\")\
\
\# 1. Load Documents\
\# We assume the user has downloaded ADK docs to \'./adk_docs\'\
def load_and_tag_documents(directory):\
reader = SimpleDirectoryReader(input_dir=directory, recursive=True)\
docs = reader.load_data()\
return docs\
\
documents = load_and_tag_documents(\"./adk_docs\")\
\
\# 2. Parse Markdown into Hierarchy (Parent Nodes)\
\# This splits by headers (\#, \#\#, \#\#\#) retaining structure\
markdown_parser = MarkdownNodeParser()\
nodes = markdown_parser.get_nodes_from_documents(documents)\
\
\# 3. Create Child Nodes (Chunks) for Retrieval\
\# We will index these smaller chunks but link them to the parent nodes\
child_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
chunk_overlap=100)\
\
all_nodes =\
for parent_node in nodes:\
\# Create child nodes from the parent\'s text\
child_nodes = child_splitter.get_nodes_from_documents()\
\
for child in child_nodes:\
\# Create an IndexNode that links back to the parent\
\# The \'index_id\' points to the parent_node.node_id\
\# The text is the child text (used for embedding)\
sub_node = IndexNode(\
text=child.text,\
index_id=parent_node.node_id,\
metadata=parent_node.metadata\
)\
all_nodes.append(sub_node)

### 6.2 Recursive Retrieval Setup

Python

from llama_index.core.retrievers import RecursiveRetriever\
from llama_index.core.query_engine import RetrieverQueryEngine\
\
\# 4. Setup Vector Store (ChromaDB)\
db = chromadb.PersistentClient(path=\"./chroma_db\")\
chroma_collection = db.get_or_create_collection(\"adk_docs\")\
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)\
storage_context =
StorageContext.from_defaults(vector_store=vector_store)\
\
\# 5. Indexing\
vector_index = VectorStoreIndex(all_nodes,
storage_context=storage_context, embed_model=embed_model)\
\
\# Create a dictionary of all nodes (parents and children) to allow ID
lookup\
node_dict = {n.node_id: n for n in nodes}\
\
\# Base Vector Retriever\
vector_retriever = vector_index.as_retriever(similarity_top_k=10)\
\
\# Recursive Retriever\
\# When the vector retriever finds an IndexNode, it looks up the
\'index_id\' in \'node_dict\'\
\# and returns that Parent Node instead.\
recursive_retriever = RecursiveRetriever(\
\"vector\",\
retriever_dict={\"vector\": vector_retriever},\
node_dict=node_dict,\
verbose=True\
)\
\
\# Reranking (Optional but Recommended)\
from llama_index.postprocessor.cohere_rerank import CohereRerank\
reranker = CohereRerank(api_key=\"YOUR_COHERE_KEY\", top_n=5)\
\
query_engine = RetrieverQueryEngine.from_args(\
retriever=recursive_retriever,\
node_postprocessors=\[reranker\],\
llm=OpenAI(model=\"gpt-4-turbo\")\
)\
\
\# Usage\
response = query_engine.query(\"How do I initialize the agent in
Python?\")\
print(response)

## 7. Implementation Guide: LangChain Pipeline

LangChain offers a streamlined class ParentDocumentRetriever that
abstracts the complexity of managing the parent-child relationship.

### 7.1 Pre-processing Script: Tab Flattener

Before feeding data to LangChain, we must handle the \"Tabbed Widget\"
issue to prevent context switching noise.

Python

import re\
\
def flatten_markdown_tabs(markdown_text):\
\"\"\"\
Detects tabbed code blocks (often HTML or specific markdown widgets)\
and converts them into sequential, labelled markdown sections.\
\"\"\"\
\# Regex to capture the tab label and content\
\# Assumes a pattern like {% tab label=\"Python\" %}\... {% endtab %}\
pattern = r\'{% tab label=\"(.\*?)\" %}(.\*?){% endtab %}\'\
\
def replacement(match):\
lang_label = match.group(1)\
code_content = match.group(2)\
\# Convert to a Header structure that the Splitter will recognize\
return f\"\\n\\n\#\#\#\# {lang_label}
Implementation\\n{code_content}\\n\"\
\
\# Remove the container tags\
text = re.sub(r\'{% tabs %}\', \'\', markdown_text)\
text = re.sub(r\'{% endtabs %}\', \'\', text)\
\# Replace tabs with headers\
text = re.sub(pattern, replacement, text, flags=re.DOTALL)\
\
return text

### 7.2 Parent Document Retriever Implementation

Python

from langchain.retrievers import ParentDocumentRetriever\
from langchain.storage import InMemoryStore \# Use RedisStore for
production\
from langchain_chroma import Chroma\
from langchain_text_splitters import RecursiveCharacterTextSplitter,
MarkdownHeaderTextSplitter\
from langchain_openai import OpenAIEmbeddings\
from langchain_core.documents import Document\
\
\# 1. Define Splitters\
\# Parent Splitter: Respects Markdown structure (Big Chunks)\
parent_splitter = MarkdownHeaderTextSplitter(\
headers_to_split_on=\[\
(\"\#\", \"Header 1\"),\
(\"\#\#\", \"Header 2\"),\
(\"\#\#\#\", \"Header 3\"),\
\]\
)\
\
\# Child Splitter: Creates \"Small\" chunks for vector search\
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400,
chunk_overlap=50)\
\
\# 2. Initialize Vectorstore (for Children) and Docstore (for Parents)\
vectorstore = Chroma(\
collection_name=\"split_parents\",\
embedding_function=OpenAIEmbeddings(model=\"text-embedding-3-large\")\
)\
store = InMemoryStore()\
\
\# 3. Initialize Retriever\
retriever = ParentDocumentRetriever(\
vectorstore=vectorstore,\
docstore=store,\
child_splitter=child_splitter,\
)\
\
\# 4. Ingestion Logic\
\# Note: ParentDocumentRetriever expects a TextSplitter for parents,\
\# but MarkdownHeaderTextSplitter returns Documents.\
\# Workaround: Pre-split parents manually and add_documents.\
\
raw_documents = \# Load using TextLoader or similar\
\
parent_docs =\
for raw_doc in raw_documents:\
\# Flatten tabs first\
cleaned_text = flatten_markdown_tabs(raw_doc.page_content)\
\# Split\
splits = parent_splitter.split_text(cleaned_text)\
\# Re-attach source metadata\
for split in splits:\
split.metadata.update(raw_doc.metadata)\
parent_docs.extend(splits)\
\
\# Add to Retriever\
\# The retriever will automatically split these \'parent_docs\' into
\'children\'\
\# index the children, and store the parents.\
retriever.add_documents(parent_docs)\
\
\# 5. Retrieval\
results = retriever.invoke(\"How to configure Spanner client in
Java?\")\
\# \'results\' contains the full parent sections, preserving context.

## 8. Evaluation and Optimization

Building the pipeline is only the first step. To ensure it meets the
requirements of professional development workflows, it must be evaluated
rigorously.

### 8.1 Ragas Framework

Use **Ragas** (Retrieval Augmented Generation Assessment) to evaluate
the pipeline\'s performance. Ragas provides metrics that correlate well
with human judgment without requiring human labeling for every query.

1.  **Context Precision:** Measures whether the retrieved code blocks
    > are relevant to the query. High precision means less noise in the
    > context window.

2.  **Context Recall:** Measures if the retrieved context contains *all*
    > the information needed to answer the query (e.g., imports,
    > variable definitions).

3.  **Faithfulness:** Measures if the generated answer is derived solely
    > from the retrieved context, preventing hallucinations where the
    > LLM invents non-existent AdK methods.

### 8.2 The \"Golden Dataset\"

Create a dataset of 50-100 pairs of (Question, Answer, Source File) to
serve as a benchmark.

-   *Question:* \"How to add memory to an agent?\"

-   *Ground Truth:* A specific code block in agents/memory.md.

-   *Metric:* Hit Rate @ k=5 (Does the correct chunk appear in the top 5
    > results?).

### 8.3 Latency vs. Accuracy Trade-offs

-   **Voyage-code-2** is slower than local embeddings but significantly
    > more accurate for code.

-   **Reranking** adds \~200-500ms latency but can double precision.

-   **Hybrid Search** requires maintaining a sparse index (more RAM) but
    > is essential for finding exact variable names.

**Production Recommendation:** Start with **Hybrid Search + OpenAI
Embeddings + No Reranker**. If accuracy is low on specific code queries,
add **Cohere Reranker**. If code understanding is still poor (e.g.,
distinguishing between similarly named functions), switch the embedding
model to **Voyage**.

## 9. Conclusion

Building a RAG pipeline for the Google AdK documentation requires moving
beyond standard text retrieval practices. The presence of mixed
code/text modalities, complex Markdown structures, and multi-language
tabs necessitates a **structure-aware ingestion strategy**.

The recommended architecture is a **Recursive Retrieval (Small-to-Big)**
system. This system parses Markdown into hierarchical sections (parents)
while indexing granular child chunks for vector similarity. By combining
this with **Hybrid Search** to capture exact code syntax and **Metadata
Filtering** to handle multi-language ambiguity, developers can build a
system that accurately answers complex technical queries with precise,
contextually complete code examples.

The code examples provided for LlamaIndex and LangChain demonstrate that
the complexity lies not in the vector store itself, but in the
**preprocessing and parsing layer**. Investing effort in \"Tab
Unrolling\" and \"Header Preservation\" yields the highest ROI for
retrieval quality. By strictly adhering to these architectural patterns,
one can transform a static documentation folder into a dynamic, highly
intelligent coding assistant.

#### Obras citadas

1.  RAG For a Codebase with 10k Repos - Qodo, fecha de acceso: enero 29,
    > 2026,
    > [[https://www.qodo.ai/blog/rag-for-large-scale-code-repos/]{.ul}](https://www.qodo.ai/blog/rag-for-large-scale-code-repos/)

2.  Chunking Strategies for LLM Applications - Pinecone, fecha de
    > acceso: enero 29, 2026,
    > [[https://www.pinecone.io/learn/chunking-strategies/]{.ul}](https://www.pinecone.io/learn/chunking-strategies/)

3.  Use Markdown in Google Docs, Slides, & Drawings, fecha de acceso:
    > enero 29, 2026,
    > [[https://support.google.com/docs/answer/12014036?hl=en]{.ul}](https://support.google.com/docs/answer/12014036?hl=en)

4.  Rethinking Markdown Splitting for RAG: Context Preservation -
    > Reddit, fecha de acceso: enero 29, 2026,
    > [[https://www.reddit.com/r/Rag/comments/1f0q2b7/rethinking_markdown_splitting_for_rag_context/]{.ul}](https://www.reddit.com/r/Rag/comments/1f0q2b7/rethinking_markdown_splitting_for_rag_context/)

5.  Split markdown - Docs by LangChain, fecha de acceso: enero 29, 2026,
    > [[https://docs.langchain.com/oss/python/integrations/splitters/markdown_header_metadata_splitter]{.ul}](https://docs.langchain.com/oss/python/integrations/splitters/markdown_header_metadata_splitter)

6.  ParentDocumentRetriever \| langchain.js, fecha de acceso: enero 29,
    > 2026,
    > [[https://reference.langchain.com/javascript/classes/\_langchain_classic.retrievers_parent_document.ParentDocumentRetriever.html]{.ul}](https://reference.langchain.com/javascript/classes/_langchain_classic.retrievers_parent_document.ParentDocumentRetriever.html)

7.  wpdevelopment11/codeblocks: Modify Markdown fenced code blocks to
    > contain the language name by detecting it from the block
    > contents. - GitHub, fecha de acceso: enero 29, 2026,
    > [[https://github.com/wpdevelopment11/codeblocks]{.ul}](https://github.com/wpdevelopment11/codeblocks)

8.  llama-index-packs-recursive-retriever - GitHub, fecha de acceso:
    > enero 29, 2026,
    > [[https://github.com/run-llama/llama_index/blob/main/llama-index-packs/llama-index-packs-recursive-retriever/README.md]{.ul}](https://github.com/run-llama/llama_index/blob/main/llama-index-packs/llama-index-packs-recursive-retriever/README.md)

9.  7 Chunking Strategies for Langchain \| by Anix Lynch, MBA, ex-VC \|
    > Medium, fecha de acceso: enero 29, 2026,
    > [[https://medium.com/\@anixlynch/7-chunking-strategies-for-langchain-b50dac194813]{.ul}](https://medium.com/@anixlynch/7-chunking-strategies-for-langchain-b50dac194813)

10. Using RAG with a Programming/API Reference Document to Write \...,
    > fecha de acceso: enero 29, 2026,
    > [[https://www.reddit.com/r/Rag/comments/1haipp8/using_rag_with_a\_programmingapi_reference/]{.ul}](https://www.reddit.com/r/Rag/comments/1haipp8/using_rag_with_a_programmingapi_reference/)

11. Text Embedding Models Compared: OpenAI, Voyage, Cohere & More -
    > Document360, fecha de acceso: enero 29, 2026,
    > [[https://document360.com/blog/text-embedding-model-analysis/]{.ul}](https://document360.com/blog/text-embedding-model-analysis/)

12. Best Embedding Model for Code + Text Documents in RAG? - Reddit,
    > fecha de acceso: enero 29, 2026,
    > [[https://www.reddit.com/r/Rag/comments/1jdmszc/best_embedding_model_for_code_text_documents_in/]{.ul}](https://www.reddit.com/r/Rag/comments/1jdmszc/best_embedding_model_for_code_text_documents_in/)

13. voyage-code-2: Elevate Your Code Retrieval, fecha de acceso: enero
    > 29, 2026,
    > [[https://blog.voyageai.com/2024/01/23/voyage-code-2-elevate-your-code-retrieval/]{.ul}](https://blog.voyageai.com/2024/01/23/voyage-code-2-elevate-your-code-retrieval/)

14. The Best Embedding Models for Information Retrieval in 2025 - DEV
    > Community, fecha de acceso: enero 29, 2026,
    > [[https://dev.to/datastax/the-best-embedding-models-for-information-retrieval-in-2025-3dp5]{.ul}](https://dev.to/datastax/the-best-embedding-models-for-information-retrieval-in-2025-3dp5)

15. Vector Databases in Action: Building a RAG Pipeline for Code Search
    > and Documentation, fecha de acceso: enero 29, 2026,
    > [[https://dzone.com/articles/vector-databases-rag-pipeline-code-search]{.ul}](https://dzone.com/articles/vector-databases-rag-pipeline-code-search)

16. Improving Llamaindex RAG performance with ranking - Cole Murray -
    > Medium, fecha de acceso: enero 29, 2026,
    > [[https://colemurray.medium.com/enhancing-rag-with-baai-bge-reranker-a-comprehensive-guide-fe994ba9f82a]{.ul}](https://colemurray.medium.com/enhancing-rag-with-baai-bge-reranker-a-comprehensive-guide-fe994ba9f82a)

17. Advanced Retrieval Pipeline for RAG (HyDE, Hybrid Search, Reranking)
    > \| Build 100% Local Retrieval, fecha de acceso: enero 29, 2026,
    > [[https://www.youtube.com/watch?v=\_ZHM4wsUwPs]{.ul}](https://www.youtube.com/watch?v=_ZHM4wsUwPs)
