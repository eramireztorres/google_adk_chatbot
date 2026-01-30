---
url: https://docs.agno.com/basics/knowledge/agents/usage/rag-with-lance-db-and-sqlite
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

RAG with LanceDB and SQLite Storage

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

# RAG with LanceDB and SQLite Storage

Copy page

Copy page

This example demonstrates how to implement RAG using LanceDB vector database with Ollama embeddings and SQLite for agent data storage, providing a complete local setup for document retrieval.

## [​](#code) Code

rag\_with\_lance\_db\_and\_sqlite.py

Copy

Ask AI

```python
from agno.agent import Agent
from agno.db.sqlite.sqlite import SqliteDb
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.ollama import Ollama
from agno.vectordb.lancedb import LanceDb

# Define the database URL where the vector database will be stored
db_url = "/tmp/lancedb"

# Configure the language model
model = Ollama(id="llama3.1:8b")

# Create Ollama embedder
embedder = OllamaEmbedder(id="nomic-embed-text", dimensions=768)

# Create the vector database
vector_db = LanceDb(
    table_name="recipes",  # Table name in the vector database
    uri=db_url,  # Location to initiate/create the vector database
    embedder=embedder,  # Without using this, it will use OpenAIChat embeddings by default
)

knowledge = Knowledge(
    vector_db=vector_db,
)

knowledge.add_content_sync(
    name="Recipes", url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
)


# Set up SQL storage for the agent's data
db = SqliteDb(db_file="data.db")

# Initialize the Agent with various configurations including the knowledge base and storage
agent = Agent(
    session_id="session_id",  # use any unique identifier to identify the run
    user_id="user",  # user identifier to identify the user
    model=model,
    knowledge=knowledge,
    db=db,
)

# Use the agent to generate and print a response to a query, formatted in Markdown
agent.print_response(
    "What is the first step of making Gluai Buat Chi from the knowledge base?",
    markdown=True,
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
pip install -U agno lancedb ollama
```

3

Setup Ollama

Copy

Ask AI

```python
# Install and start Ollama
# Pull required models
ollama pull llama3.1:8b
ollama pull nomic-embed-text
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
touch rag_with_lance_db_and_sqlite.py
```

6

Run Agent

Mac

Windows

Copy

Ask AI

```python
python rag_with_lance_db_and_sqlite.py
```

7

Find All Cookbooks

Explore all the available cookbooks in the Agno repository. Click the link below to view the code on GitHub:[Agno Cookbooks on GitHub](https://github.com/agno-agi/agno/tree/main/cookbook/agents/rag)

Was this page helpful?

YesNo

[Suggest edits](https://github.com/agno-agi/agno-docs/edit/main/basics/knowledge/agents/usage/rag-with-lance-db-and-sqlite.mdx)[Raise issue](https://github.com/agno-agi/agno-docs/issues/new?title=Issue on docs&body=Path: /basics/knowledge/agents/usage/rag-with-lance-db-and-sqlite)

[RAG with Sentence Transformer Reranker](/basics/knowledge/agents/usage/rag-sentence-transformer)[Traditional RAG with LanceDB](/basics/knowledge/agents/usage/traditional-rag-lancedb)

⌘I

[x](https://x.com/AgnoAgi)[github](https://github.com/agno-agi/agno)[discord](https://agno.link/discord)[youtube](https://agno.link/youtube)[website](https://agno.com)

[Powered by Mintlify](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=agno-v2)