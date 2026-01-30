---
url: https://docs.agno.com/basics/knowledge/agents/usage/rag-sentence-transformer
source: Universal Doc Downloader
---

[Skip to main content](#content-area)

[Agno home page![light logo](https://mintcdn.com/agno-v2/yeT29TzCG5roT0hQ/logo/black.svg?fit=max&auto=format&n=yeT29TzCG5roT0hQ&q=85&s=a6afd99095eb38a8797b215b10a4944d)![dark logo](https://mintcdn.com/agno-v2/yeT29TzCG5roT0hQ/logo/white.svg?fit=max&auto=format&n=yeT29TzCG5roT0hQ&q=85&s=dd3d606ef000b66252d19edf387dc7fc)](/)

Search...

⌘K

* [Github](https://github.com/agno-agi/agno)
* [Try AgentOS](https://os.agno.com)
* [Try AgentOS](https://os.agno.com)

Search...

Navigation

Usage

RAG with Sentence Transformer Reranker

[Home](/)[Documentation](/introduction)[AgentOS](/agent-os/introduction)[Examples](/examples/use-cases/agents/overview)[Reference](/reference/agents/agent)[Deploy](/deploy/overview)[FAQs](/faq/environment-variables)

##### Get Started

* [What is Agno?](/introduction)
* [Quickstart](/get-started/quickstart)
* [Performance](/get-started/performance)
* [Getting Help](/get-started/getting-help)

##### Basics

* Agents
* Teams
* Workflows
* Input & Output
* Sessions
* Database
* Models
* Tools

##### Context Management

* Context Engineering
* Chat History
* State Management
* Context Compressionbeta
* Knowledge

  + [Overview](/basics/knowledge/overview)
  + [How Knowledge Works](/basics/knowledge/how-it-works)
  + Getting Started
  + Agents with Knowledge

    - [Overview](/basics/knowledge/agents/overview)
    - Usage

      * [Agentic RAG with LanceDB](/basics/knowledge/agents/usage/agentic-rag-lancedb)
      * [Agentic RAG with PgVector](/basics/knowledge/agents/usage/agentic-rag-pgvector)
      * [Agentic RAG with Reranking](/basics/knowledge/agents/usage/agentic-rag-with-reranking)
      * [RAG with Sentence Transformer Reranker](/basics/knowledge/agents/usage/rag-sentence-transformer)
      * [RAG with LanceDB and SQLite Storage](/basics/knowledge/agents/usage/rag-with-lance-db-and-sqlite)
      * [Traditional RAG with LanceDB](/basics/knowledge/agents/usage/traditional-rag-lancedb)
      * [Traditional RAG with PgVector](/basics/knowledge/agents/usage/traditional-rag-pgvector)
  + Teams with Knowledge
  + [Terminology](/basics/knowledge/terminology)
  + [Knowledge Bases](/basics/knowledge/knowledge-bases)
  + [Content Types](/basics/knowledge/content-types)
  + [Contents DB](/basics/knowledge/content-db)
  + Search & Retrieval
  + Readers
  + Chunking
  + Embeddings
  + Filtering Results
  + [Vector Databases](/basics/vectordb/overview)
  + [Performance Quick Wins](/basics/knowledge/performance-tips)
* Memory
* Cultureexperimental
* Dependency Injection

##### Execution Control

* Hooks
* Guardrails
* Human-in-the-Loop
* Run Cancellation

##### Additional Features

* Reasoning
* Multimodal
* Tracingbeta
* Evals
* [Custom Logging](/basics/custom-logging)
* [Telemetry](/basics/telemetry)
* [AgentUI](/basics/agent-ui/overview)

##### Integrations

* Model Providers
* Database Providers
* Vector Databases
* Toolkits
* Memory
* Observability
* Other Integrations

##### Help

* [Agno Install & Setup](/how-to/install)
* Migrate to Agno v2
* [Workflows 2.0 Migration Guide](/how-to/workflows-migration)
* [Cursor Rules](/how-to/cursor-rules)
* [Contributing to Agno](/how-to/contribute)

On this page

* [Code](#code)
* [Usage](#usage)

Usage

# RAG with Sentence Transformer Reranker

Copy page

Copy page

This example demonstrates Agentic RAG using Sentence Transformer Reranker with multilingual data for improved search relevance.

## [​](#code) Code

rag\_sentence\_transformer.py

Copy

Ask AI

```python
"""This cookbook is an implementation of Agentic RAG using Sentence Transformer Reranker with multilingual data.

## Setup Instructions:

### 1. Install Dependencies
Run: `pip install agno sentence-transformers`

### 2. Start the Postgres Server with pgvector
Run: `sh cookbook/scripts/run_pgvector.sh`

### 3. Run the example
Run: `uv run cookbook/agent_basics/rag/rag_sentence_transformer.py`
"""

from agno.agent import Agent
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reranker import SentenceTransformerReranker
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector

search_results = [
    "Organic skincare for sensitive skin with aloe vera and chamomile.",
    "New makeup trends focus on bold colors and innovative techniques",
    "Bio-Hautpflege für empfindliche Haut mit Aloe Vera und Kamille",
    "Neue Make-up-Trends setzen auf kräftige Farben und innovative Techniken",
    "Cuidado de la piel orgánico para piel sensible con aloe vera y manzanilla",
    "Las nuevas tendencias de maquillaje se centran en colores vivos y técnicas innovadoras",
    "针对敏感肌专门设计的天然有机护肤产品",
    "新的化妆趋势注重鲜艳的颜色和创新的技巧",
    "敏感肌のために特別に設計された天然有機スキンケア製品",
    "新しいメイクのトレンドは鮮やかな色と革新的な技術に焦点を当てています",
]

knowledge = Knowledge(
    vector_db=PgVector(
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        table_name="sentence_transformer_rerank_docs",
        embedder=SentenceTransformerEmbedder(
            id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        ),
    ),
    reranker=SentenceTransformerReranker(model="BAAI/bge-reranker-v2-m3"),
)

for result in search_results:
    knowledge.add_content_sync(
        content=result,
        metadata={
            "source": "search_results",
        },
    )

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    knowledge=knowledge,
    search_knowledge=True,
    instructions=[
        "Include sources in your response.",
        "Always search your knowledge before answering the question.",
    ],
    markdown=True,
)

if __name__ == "__main__":
    test_queries = [
        "What organic skincare products are good for sensitive skin?",
        "Tell me about makeup trends in different languages",
        "Compare skincare and makeup information across languages",
    ]

    for query in test_queries:
        agent.print_response(
            query,
            stream=True,
            show_full_reasoning=True,
        )
```

## [​](#usage) Usage

1

Create a virtual environment

Open the `Terminal` and create a python virtual environment.

Mac

Windows

Copy

Ask AI

```python
python3 -m venv .venv
source .venv/bin/activate
```

2

Install libraries

Copy

Ask AI

```python
pip install -U agno sentence-transformers
```

3

Start Postgres with pgvector

Copy

Ask AI

```python
sh run_pgvector.sh
```

4

Export your OpenAI API key

Mac/Linux

Windows

Copy

Ask AI

```python
  export OPENAI_API_KEY="your_openai_api_key_here"
```

5

Create a Python file

Create a Python file and add the above code.

Copy

Ask AI

```python
touch rag_sentence_transformer.py
```

6

Run Agent

Mac

Windows

Copy

Ask AI

```python
python rag_sentence_transformer.py
```

7

Find All Cookbooks

Explore all the available cookbooks in the Agno repository. Click the link below to view the code on GitHub:[Agno Cookbooks on GitHub](https://github.com/agno-agi/agno/tree/main/cookbook/agents/rag)

Was this page helpful?

YesNo

[Suggest edits](https://github.com/agno-agi/agno-docs/edit/main/basics/knowledge/agents/usage/rag-sentence-transformer.mdx)[Raise issue](https://github.com/agno-agi/agno-docs/issues/new?title=Issue on docs&body=Path: /basics/knowledge/agents/usage/rag-sentence-transformer)

[Agentic RAG with Reranking](/basics/knowledge/agents/usage/agentic-rag-with-reranking)[RAG with LanceDB and SQLite Storage](/basics/knowledge/agents/usage/rag-with-lance-db-and-sqlite)

⌘I

[x](https://x.com/AgnoAgi)[github](https://github.com/agno-agi/agno)[discord](https://agno.link/discord)[youtube](https://agno.link/youtube)[website](https://agno.com)

[Powered by Mintlify](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=agno-v2)