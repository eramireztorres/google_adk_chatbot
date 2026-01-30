---
url: https://framework.beeai.dev/modules/rag
source: Universal Doc Downloader
---

[Skip to main content](#content-area)

[BeeAI Framework home page![light logo](https://mintcdn.com/beeai-framework/nLL-ZEjrgugIyhoR/logo/beeai-framework-light.svg?fit=max&auto=format&n=nLL-ZEjrgugIyhoR&q=85&s=f0d0d501b59c56891ae141ab1811c37f)![dark logo](https://mintcdn.com/beeai-framework/nLL-ZEjrgugIyhoR/logo/beeai-framework-dark.svg?fit=max&auto=format&n=nLL-ZEjrgugIyhoR&q=85&s=b50f5c02a26bbcc6ee07b569ae30b711)](/)

Search...

⌘K

##### Introduction

* [Welcome](/introduction/welcome)
* [Quickstart](/introduction/quickstart)
* [The Grand Tour](/introduction/tour)

##### Core Concepts

* [Requirement Agent](/modules/agents/requirement-agent)
* [Middleware](/modules/middleware)
* [Agents](/modules/agents)
* [Serve](/modules/serve)
* [Backend](/modules/backend)
* [Tools](/modules/tools)
* [Memory](/modules/memory)
* [RAG](/modules/rag)
* [Observability](/modules/observability)
* [Cache](/modules/cache)
* [Logger](/modules/logger)
* [Serialization](/modules/serialization)
* [Errors](/modules/errors)
* [Templates](/modules/templates)
* [Workflows](/modules/workflows)

##### Integrations

* [Agent Stack](/integrations/agent-stack)
* [MCP](/integrations/mcp)
* [A2A](/integrations/a2a)
* [IBM watsonx Orchestrate](/integrations/watsonx-orchestrate)
* [OpenAI API](/integrations/openai-api)

##### Guides

* [MCP Slackbot](/guides/mcp-slackbot)

##### Community

* [Contribute](/community/contribute)

* [Discord](https://discord.gg/AZFrp3UF5k)
* [GitHub](https://github.com/i-am-bee/beeai-framework)

[BeeAI Framework home page![light logo](https://mintcdn.com/beeai-framework/nLL-ZEjrgugIyhoR/logo/beeai-framework-light.svg?fit=max&auto=format&n=nLL-ZEjrgugIyhoR&q=85&s=f0d0d501b59c56891ae141ab1811c37f)![dark logo](https://mintcdn.com/beeai-framework/nLL-ZEjrgugIyhoR/logo/beeai-framework-dark.svg?fit=max&auto=format&n=nLL-ZEjrgugIyhoR&q=85&s=b50f5c02a26bbcc6ee07b569ae30b711)](/)

Search...

⌘K

* [Discord](https://discord.gg/AZFrp3UF5k)
* [GitHub](https://github.com/i-am-bee/beeai-framework)
* [GitHub](https://github.com/i-am-bee/beeai-framework)

Search...

Navigation

Core Concepts

RAG

Core Concepts

# RAG

Build intelligent agents that combine retrieval with generation for enhanced AI capabilities

## [​](#overview) Overview

Retrieval-Augmented Generation (RAG) is a powerful paradigm that enhances large language models by providing them with relevant information from external knowledge sources. This approach has become essential for enterprise AI applications that need to work with specific, up-to-date, or domain-specific information that wasn’t part of the model’s training data.
RAG addresses key limitations of traditional LLMs:

* **Knowledge cutoffs** - Access the most current information
* **Domain expertise** - Integrate specialized knowledge bases
* **Factual accuracy** - Reduce hallucinations with grounded responses
* **Scalability** - Work with vast document collections efficiently

Enterprises rely on RAG for applications like customer support, document analysis, knowledge management, and intelligent search systems.

Location within the framework: [beeai\_framework/rag](https://github.com/i-am-bee/beeai-framework/blob/main/python/beeai_framework/rag).

RAG is most effective when document chunking and retrieval strategies are tailored to your specific problem domain. It’s recommended to experiment with different configurations such as chunk sizes, overlap settings, and retrieval parameters. Future releases of BeeAI will provide enhanced capabilities to streamline this optimization process.

## [​](#philosophy) Philosophy

BeeAI Framework’s approach to RAG emphasizes **integration over invention**. Rather than building RAG components from scratch, we provide seamless adapters for proven, production-ready solutions from leading platforms like LangChain and Llama-Index.
This philosophy offers several advantages:

* **Leverage existing expertise** - Use battle-tested implementations
* **Faster time-to-market** - Focus on your application logic, not infrastructure
* **Community support** - Benefit from extensive documentation and community
* **Flexibility** - Switch between providers as needs evolve

## [​](#installation) Installation

To use RAG components, install the framework with the RAG extras:

Copy

Ask AI

```python
pip install "beeai-framework[rag]"
```

## [​](#rag-components) RAG Components

The following table outlines the key RAG components available in the BeeAI Framework:

| Component | Description | Compatibility | Future Compatibility |
| --- | --- | --- | --- |
| [**Document Loaders**](https://github.com/i-am-bee/beeai-framework/blob/main/python/beeai_framework/backend/document_loader.py) | Responsible for loading content from different formats and sources such as PDFs, web pages, and structured text files | LangChain | BeeAI |
| [**Text Splitters**](https://github.com/i-am-bee/beeai-framework/blob/main/python/beeai_framework/backend/text_splitter.py) | Splits long documents into workable chunks using various strategies, e.g. fixed length or preserving context | LangChain | BeeAI |
| [**Document**](https://github.com/i-am-bee/beeai-framework/blob/main/python/beeai_framework/backend/types.py) | The basic data structure to house text content, metadata, and relevant scores for retrieval operations | BeeAI | - |
| [**Vector Store**](https://github.com/i-am-bee/beeai-framework/blob/main/python/beeai_framework/backend/vector_store.py) | Used to store document embeddings and retrieve them based on semantic similarity using embedding distance | LangChain | BeeAI, Llama-Index |
| [**Document Processors**](https://github.com/i-am-bee/beeai-framework/blob/main/python/beeai_framework/backend/document_processor.py) | Used to process and refine documents during the retrieval-generation lifecycle including reranking and filtering | Llama-Index | - |

## [​](#dynamic-module-loading) Dynamic Module Loading

BeeAI Framework provides a dynamic module loading system that allows you to instantiate RAG components using string identifiers. This approach enables configuration-driven architectures and easy provider switching.
The `from_name` method uses the format `provider:ClassName` where:

* `provider` identifies the integration module (e.g., “beeai”, “langchain”)
* `ClassName` specifies the exact class to instantiate

Dynamic loading enables you to switch between different vector store implementations without changing your application code - just update the configuration string.

### [​](#beeai-vector-store) BeeAI Vector Store

Python

Copy

Ask AI

```python
import asyncio
import sys
import traceback

from beeai_framework.adapters.beeai.backend.vector_store import TemporalVectorStore
from beeai_framework.adapters.langchain.mappers.documents import lc_document_to_document
from beeai_framework.backend.embedding import EmbeddingModel
from beeai_framework.backend.vector_store import VectorStore
from beeai_framework.errors import FrameworkError

# LC dependencies - to be swapped with BAI dependencies
try:
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "Optional modules are not found.\nRun 'pip install \"beeai-framework[rag]\"' to install."
    ) from e


async def main() -> None:
    embedding_model = EmbeddingModel.from_name("watsonx:ibm/slate-125m-english-rtrvr-v2", truncate_input_tokens=500)

    # Document loading
    loader = UnstructuredMarkdownLoader(file_path="docs/modules/agents.mdx")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=1000)
    all_splits = text_splitter.split_documents(docs)
    documents = [lc_document_to_document(document) for document in all_splits]
    print(f"Loaded {len(documents)} documents")

    vector_store: TemporalVectorStore = VectorStore.from_name(
        name="beeai:TemporalVectorStore", embedding_model=embedding_model
    )  # type: ignore[assignment]
    _ = await vector_store.add_documents(documents=documents)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
```

See all 44 lines

Native BeeAI modules can be loaded directly by importing and instantiating the module, e.g. `from beeai_framework.adapters.beeai.backend.vector_store import TemporalVectorStore`.

### [​](#supported-provider’s-vector-store) Supported Provider’s Vector Store

Python

Python

Copy

Ask AI

```python
# LangChain integration
vector_store = VectorStore.from_name(
    name="langchain:InMemoryVectorStore",
    embedding_model=embedding_model
)
```

See all 5 lines

For production deployments, consider implementing document caching and index optimization to improve response times.

### [​](#rag-as-tools) RAG as Tools

Vector store population (loading and chunking documents) is typically handled offline in production applications, making Vector Store the prominent RAG building block utilized as a tool.
`VectorStoreSearchTool` enables any agent to perform semantic search against a pre-populated vector store. This provides flexibility for agents that need retrieval capabilities alongside other functionalities.

The VectorStoreSearchTool can be dynamically instantiated using `VectorStoreSearchTool.from_vector_store_name("beeai:TemporalVectorStore", embedding_model=embedding_model)`, see RAG with RequirementAgent example for the full code.

## [​](#examples) Examples

[## Python RAG Agent

Complete RAG agent implementation with document loading and processing](https://github.com/i-am-bee/beeai-framework/tree/main/python/examples/agents/rag_agent.py)

[## RAG with RequirementAgent

Example showing how to use VectorStoreSearchTool with RequirementAgent for RAG capabilities](https://github.com/i-am-bee/beeai-framework/tree/main/python/examples/agents/requirement/rag.py)

Was this page helpful?

YesNo

[Previous](/modules/memory)[ObservabilityMonitor and debug your BeeAI Framework applications with OpenInference instrumentation

Next](/modules/observability)

⌘I

[github](https://github.com/i-am-bee/beeai-framework)[discord](https://discord.gg/NradeA6ZNF)[bluesky](https://bsky.app/profile/beeaiagents.bsky.social)[youtube](https://www.youtube.com/@BeeAIAgents)

On this page

* [Overview](#overview)
* [Philosophy](#philosophy)
* [Installation](#installation)
* [RAG Components](#rag-components)
* [Dynamic Module Loading](#dynamic-module-loading)
* [BeeAI Vector Store](#beeai-vector-store)
* [Supported Provider’s Vector Store](#supported-provider%E2%80%99s-vector-store)
* [RAG Agent](#rag-agent)
* [1. Retrieval](#1-retrieval)
* [2. Reranking (Optional)](#2-reranking-optional)
* [3. Generation](#3-generation)
* [Basic Usage](#basic-usage)
* [RAG as Tools](#rag-as-tools)
* [Examples](#examples)