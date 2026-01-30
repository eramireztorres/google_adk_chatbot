---
url: https://docs.agno.com/basics/knowledge/teams/usage/distributed-rag-with-reranking
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

Distributed RAG

Distributed RAG with Advanced Reranking

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
  + Teams with Knowledge

    - [Overview](/basics/knowledge/teams/overview)
    - Usage

      * [Team with Knowledge Base](/basics/knowledge/teams/usage/team-with-knowledge)
      * [Team with Knowledge Filters](/basics/knowledge/teams/usage/team-with-knowledge-filters)
      * [Team with Agentic Knowledge Filters](/basics/knowledge/teams/usage/team-with-agentic-knowledge-filters)
      * Distributed RAG

        + [Distributed RAG with PgVector](/basics/knowledge/teams/usage/distributed-rag-pgvector)
        + [Distributed RAG with LanceDB](/basics/knowledge/teams/usage/distributed-rag-lancedb)
        + [Distributed RAG with Reranking](/basics/knowledge/teams/usage/distributed-rag-with-reranking)
      * Search Coordination
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

Distributed RAG

# Distributed RAG with Advanced Reranking

Copy page

Copy page

This example demonstrates how multiple specialized agents coordinate to provide comprehensive RAG responses using advanced reranking strategies for optimal information retrieval and synthesis. The team includes initial retrieval, reranking optimization, context analysis, and final synthesis.

## [​](#code) Code

cookbook/examples/teams/distributed\_rag/03\_distributed\_rag\_with\_reranking.py

Copy

Ask AI

```python
"""
This example demonstrates how multiple specialized agents coordinate to provide
comprehensive RAG responses using advanced reranking strategies for optimal
information retrieval and synthesis.

Team Composition:
- Initial Retriever: Performs broad initial retrieval from knowledge base
- Reranking Specialist: Applies advanced reranking for result optimization
- Context Analyzer: Analyzes context and relevance of reranked results
- Final Synthesizer: Synthesizes reranked results into optimal responses

Setup:
1. Run: `pip install openai lancedb tantivy pypdf sqlalchemy agno`
2. Run this script to see advanced reranking RAG in action
"""

import asyncio

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reranker.cohere import CohereReranker
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.utils.print_response.team import aprint_response, print_response
from agno.vectordb.lancedb import LanceDb, SearchType

# Knowledge base with advanced reranking
reranked_knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="recipes_reranked",
        uri="tmp/lancedb",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        reranker=CohereReranker(model="rerank-v3.5"),
    ),
)

# Secondary knowledge base for cross-validation
validation_knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="recipes_validation",
        uri="tmp/lancedb",
        search_type=SearchType.vector,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)

# Initial Retriever Agent - Specialized in broad initial retrieval
initial_retriever = Agent(
    name="Initial Retriever",
    model=OpenAIChat(id="gpt-5-mini"),
    role="Perform broad initial retrieval to gather candidate information",
    knowledge=reranked_knowledge,
    search_knowledge=True,
    instructions=[
        "Perform comprehensive initial retrieval from the knowledge base.",
        "Cast a wide net to gather all potentially relevant information.",
        "Focus on recall rather than precision in this initial phase.",
        "Retrieve diverse content that might be relevant to the query.",
    ],
    markdown=True,
)

# Reranking Specialist Agent - Specialized in result optimization
reranking_specialist = Agent(
    name="Reranking Specialist",
    model=OpenAIChat(id="gpt-5-mini"),
    role="Apply advanced reranking to optimize retrieval results",
    knowledge=reranked_knowledge,
    search_knowledge=True,
    instructions=[
        "Apply advanced reranking techniques to optimize result relevance.",
        "Focus on precision and ranking quality over quantity.",
        "Use the Cohere reranker to identify the most relevant content.",
        "Prioritize results that best match the user's specific needs.",
    ],
    markdown=True,
)

# Context Analyzer Agent - Specialized in context analysis
context_analyzer = Agent(
    name="Context Analyzer",
    model=OpenAIChat(id="gpt-5-mini"),
    role="Analyze context and relevance of reranked results",
    knowledge=validation_knowledge,
    search_knowledge=True,
    instructions=[
        "Analyze the context and relevance of reranked results.",
        "Cross-validate information against the validation knowledge base.",
        "Assess the quality and accuracy of retrieved content.",
        "Identify the most contextually appropriate information.",
    ],
    markdown=True,
)

# Final Synthesizer Agent - Specialized in optimal synthesis
final_synthesizer = Agent(
    name="Final Synthesizer",
    model=OpenAIChat(id="gpt-5-mini"),
    role="Synthesize reranked results into optimal comprehensive responses",
    instructions=[
        "Synthesize information from all team members into optimal responses.",
        "Leverage the reranked and analyzed results for maximum quality.",
        "Create responses that demonstrate the benefits of advanced reranking.",
        "Ensure optimal information organization and presentation.",
        "Include confidence levels and source quality indicators.",
    ],
    markdown=True,
)

# Create distributed reranking RAG team
distributed_reranking_team = Team(
    name="Distributed Reranking RAG Team",
    model=OpenAIChat(id="gpt-5-mini"),
    members=[
        initial_retriever,
        reranking_specialist,
        context_analyzer,
        final_synthesizer,
    ],
    instructions=[
        "Work together to provide optimal RAG responses using advanced reranking.",
        "Initial Retriever: First perform broad comprehensive retrieval.",
        "Reranking Specialist: Apply advanced reranking for result optimization.",
        "Context Analyzer: Analyze and validate the reranked results.",
        "Final Synthesizer: Create optimal responses from reranked information.",
        "Leverage advanced reranking for superior result quality.",
        "Demonstrate the benefits of specialized reranking in team coordination.",
    ],
    show_members_responses=True,
    markdown=True,
)


async def async_reranking_rag_demo():
    """Demonstrate async distributed reranking RAG processing."""
    print("🎯 Async Distributed Reranking RAG Demo")
    print("=" * 45)

    query = "What's the best way to prepare authentic Tom Kha Gai? I want traditional methods and modern variations."

    # Add content to knowledge bases
    await reranked_knowledge.add_contents_async(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
    )
    await validation_knowledge.add_contents_async(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
    )

    # Run async distributed reranking RAG
    await aprint_response(input=query, team=distributed_reranking_team)


def sync_reranking_rag_demo():
    """Demonstrate sync distributed reranking RAG processing."""
    print("🎯 Distributed Reranking RAG Demo")
    print("=" * 35)

    query = "What's the best way to prepare authentic Tom Kha Gai? I want traditional methods and modern variations."

    # Add content to knowledge bases
    reranked_knowledge.add_contents(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
    )
    validation_knowledge.add_contents(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
    )

    # Run distributed reranking RAG
    print_response(distributed_reranking_team, query)


def advanced_culinary_demo():
    """Demonstrate advanced reranking for complex culinary queries."""
    print("👨‍🍳 Advanced Culinary Analysis with Reranking RAG")
    print("=" * 55)

    query = """I want to understand the science behind Thai curry pastes. Can you explain:
    - Traditional preparation methods vs modern techniques
    - How different ingredients affect flavor profiles
    - Regional variations and their historical origins
    - Best practices for storage and usage
    - How to adapt recipes for different dietary needs"""

    # Add content to knowledge bases
    reranked_knowledge.add_contents(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
    )
    validation_knowledge.add_contents(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
    )

    print_response(distributed_reranking_team, query)


if __name__ == "__main__":
    # Choose which demo to run
    asyncio.run(async_reranking_rag_demo())

    # advanced_culinary_demo()

    # sync_reranking_rag_demo()
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

Install required libraries

Copy

Ask AI

```python
pip install agno openai lancedb tantivy pypdf sqlalchemy cohere
```

3

Set environment variables

Copy

Ask AI

```python
export OPENAI_API_KEY=****
export COHERE_API_KEY=****
```

4

Run the agent

Copy

Ask AI

```python
python cookbook/examples/teams/distributed_rag/03_distributed_rag_with_reranking.py
```

Was this page helpful?

YesNo

[Suggest edits](https://github.com/agno-agi/agno-docs/edit/main/basics/knowledge/teams/usage/distributed-rag-with-reranking.mdx)[Raise issue](https://github.com/agno-agi/agno-docs/issues/new?title=Issue on docs&body=Path: /basics/knowledge/teams/usage/distributed-rag-with-reranking)

[Distributed RAG with LanceDB](/basics/knowledge/teams/usage/distributed-rag-lancedb)[Coordinated Agentic RAG Team](/basics/knowledge/teams/usage/coordinated-agentic-rag)

⌘I

[x](https://x.com/AgnoAgi)[github](https://github.com/agno-agi/agno)[discord](https://agno.link/discord)[youtube](https://agno.link/youtube)[website](https://agno.com)

[Powered by Mintlify](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=agno-v2)