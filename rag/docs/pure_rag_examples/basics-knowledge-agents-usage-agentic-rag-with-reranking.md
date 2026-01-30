---
url: https://docs.agno.com/basics/knowledge/agents/usage/agentic-rag-with-reranking
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

Agentic RAG with Reranking

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

# Agentic RAG with Reranking

Copy page

Copy page

This example demonstrates how to implement Agentic RAG using LanceDB with Cohere reranking for improved search results.

## [​](#code) Code

agentic\_rag\_with\_reranking.py

Copy

Ask AI

```python
"""
1. Run: `pip install openai agno cohere lancedb tantivy sqlalchemy pandas` to install the dependencies
2. Export your OPENAI_API_KEY and CO_API_KEY
3. Run: `python cookbook/agent_basics/rag/agentic_rag_with_reranking.py` to run the agent
"""

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reranker.cohere import CohereReranker
from agno.models.openai import OpenAIChat
from agno.vectordb.lancedb import LanceDb, SearchType

knowledge = Knowledge(
    # Use LanceDB as the vector database and store embeddings in the `agno_docs` table
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small"
        ),  # Use OpenAI for embeddings
        reranker=CohereReranker(
            model="rerank-multilingual-v3.0"
        ),  # Use Cohere for reranking
    ),
)

knowledge.add_content_sync(
    name="Agno Docs", url="https://docs.agno.com/introduction.md"
)

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    # Agentic RAG is enabled by default when `knowledge` is provided to the Agent.
    knowledge=knowledge,
    markdown=True,
)

if __name__ == "__main__":
    # Load the knowledge base, comment after first run
    # agent.knowledge.load(recreate=True)
    agent.print_response("What are Agno's key features?")
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
pip install -U agno cohere lancedb tantivy sqlalchemy pandas
```

3

Set environment variables

Copy

Ask AI

```python
export OPENAI_API_KEY=your_openai_api_key
export CO_API_KEY=your_cohere_api_key
```

4

Create a Python file

Create a Python file and add the above code.

Copy

Ask AI

```python
touch agentic_rag_with_reranking.py
```

5

Run Agent

Mac

Windows

Copy

Ask AI

```python
python agentic_rag_with_reranking.py
```

6

Find All Cookbooks

Explore all the available cookbooks in the Agno repository. Click the link below to view the code on GitHub:[Agno Cookbooks on GitHub](https://github.com/agno-agi/agno/tree/main/cookbook/agents/rag)

Was this page helpful?

YesNo

[Suggest edits](https://github.com/agno-agi/agno-docs/edit/main/basics/knowledge/agents/usage/agentic-rag-with-reranking.mdx)[Raise issue](https://github.com/agno-agi/agno-docs/issues/new?title=Issue on docs&body=Path: /basics/knowledge/agents/usage/agentic-rag-with-reranking)

[Agentic RAG with PgVector](/basics/knowledge/agents/usage/agentic-rag-pgvector)[RAG with Sentence Transformer Reranker](/basics/knowledge/agents/usage/rag-sentence-transformer)

⌘I

[x](https://x.com/AgnoAgi)[github](https://github.com/agno-agi/agno)[discord](https://agno.link/discord)[youtube](https://agno.link/youtube)[website](https://agno.com)

[Powered by Mintlify](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=agno-v2)