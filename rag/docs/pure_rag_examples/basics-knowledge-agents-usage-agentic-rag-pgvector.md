---
url: https://docs.agno.com/basics/knowledge/agents/usage/agentic-rag-pgvector
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

Agentic RAG with PgVector

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

# Agentic RAG with PgVector

Copy page

Copy page

This example demonstrates how to implement Agentic RAG using PgVector (PostgreSQL with vector extensions) for storing and searching embeddings with hybrid search capabilities.

## [​](#code) Code

agentic\_rag\_pgvector.py

Copy

Ask AI

```python
"""
1. Run: `./cookbook/run_pgvector.sh` to start a postgres container with pgvector
2. Run: `pip install openai sqlalchemy 'psycopg[binary]' pgvector agno` to install the dependencies
3. Run: `python cookbook/rag/02_agentic_rag_pgvector.py` to run the agent
"""

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector, SearchType

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
knowledge = Knowledge(
    # Use PgVector as the vector database and store embeddings in the `ai.recipes` table
    vector_db=PgVector(
        table_name="recipes",
        db_url=db_url,
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)

knowledge.add_content(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
)

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    knowledge=knowledge,
    # Add a tool to search the knowledge base which enables agentic RAG.
    # This is enabled by default when `knowledge` is provided to the Agent.
    search_knowledge=True,
    markdown=True,
)
agent.print_response(
    "How do I make chicken and galangal in coconut milk soup", stream=True
)
# agent.print_response(
#     "Hi, i want to make a 3 course meal. Can you recommend some recipes. "
#     "I'd like to start with a soup, then im thinking a thai curry for the main course and finish with a dessert",
#     stream=True,
# )
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
pip install -U agno openai sqlalchemy psycopg2-binary pgvector
```

3

Setup PgVector

Copy

Ask AI

```python
# Start PostgreSQL with pgvector extension
# Update connection string in the code as needed
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
touch agentic_rag_pgvector.py
```

6

Run Agent

Mac

Windows

Copy

Ask AI

```python
python agentic_rag_pgvector.py
```

7

Find All Cookbooks

Explore all the available cookbooks in the Agno repository. Click the link below to view the code on GitHub:[Agno Cookbooks on GitHub](https://github.com/agno-agi/agno/tree/main/cookbook/agents/rag)

Was this page helpful?

YesNo

[Suggest edits](https://github.com/agno-agi/agno-docs/edit/main/basics/knowledge/agents/usage/agentic-rag-pgvector.mdx)[Raise issue](https://github.com/agno-agi/agno-docs/issues/new?title=Issue on docs&body=Path: /basics/knowledge/agents/usage/agentic-rag-pgvector)

[Agentic RAG with LanceDB](/basics/knowledge/agents/usage/agentic-rag-lancedb)[Agentic RAG with Reranking](/basics/knowledge/agents/usage/agentic-rag-with-reranking)

⌘I

[x](https://x.com/AgnoAgi)[github](https://github.com/agno-agi/agno)[discord](https://agno.link/discord)[youtube](https://agno.link/youtube)[website](https://agno.com)

[Powered by Mintlify](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=agno-v2)