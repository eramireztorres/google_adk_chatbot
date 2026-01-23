---
url: https://google.github.io/adk-docs/sessions/
source: Google ADK Documentation
---

[adk-python](https://github.com/google/adk-python "adk-python")

[adk-go](https://github.com/google/adk-go "adk-go")

[adk-java](https://github.com/google/adk-java "adk-java")

* [Home](..)

  Home
* Build Agents




  Build Agents
  + [Get Started](../get-started/)

    Get Started
    - [Python](../get-started/python/)
    - [Go](../get-started/go/)
    - [Java](../get-started/java/)
  + [Build your Agent](../tutorials/)

    Build your Agent
    - [Multi-tool agent](../get-started/quickstart/)
    - [Agent team](../tutorials/agent-team/)
    - [Streaming agent](../get-started/streaming/)

      Streaming agent
      * [Python](../get-started/streaming/quickstart-streaming/)
      * [Java](../get-started/streaming/quickstart-streaming-java/)
    - [Visual Builder](../visual-builder/)
    - [Advanced setup](../get-started/installation/)
  + [Agents](../agents/)

    Agents
    - [LLM agents](../agents/llm-agents/)
    - [Workflow agents](../agents/workflow-agents/)

      Workflow agents
      * [Sequential agents](../agents/workflow-agents/sequential-agents/)
      * [Loop agents](../agents/workflow-agents/loop-agents/)
      * [Parallel agents](../agents/workflow-agents/parallel-agents/)
    - [Custom agents](../agents/custom-agents/)
    - [Multi-agent systems](../agents/multi-agents/)
    - [Agent Config](../agents/config/)
    - [Models & Authentication](../agents/models/)
  + [Tools for Agents](../tools/)

    Tools for Agents
    - [Built-in tools](../tools/built-in-tools/)
    - Gemini API tools




      Gemini API tools
      * [Computer use](../tools/gemini-api/computer-use/)
    - Google Cloud tools




      Google Cloud tools
      * [Overview](../tools/google-cloud-tools/)
      * [MCP Toolbox for Databases](../tools/google-cloud/mcp-toolbox-for-databases/)
      * [BigQuery Agent Analytics](../tools/google-cloud/bigquery-agent-analytics/)
      * [Code Execution with Agent Engine](../tools/google-cloud/code-exec-agent-engine/)
    - [Third-party tools](../tools/third-party/)

      Third-party tools
      * [AgentQL](../tools/third-party/agentql/)
      * [Bright Data](../tools/third-party/bright-data/)
      * [Browserbase](../tools/third-party/browserbase/)
      * [Exa](../tools/third-party/exa/)
      * [Firecrawl](../tools/third-party/firecrawl/)
      * [GitHub](../tools/third-party/github/)
      * [Hugging Face](../tools/third-party/hugging-face/)
      * [Notion](../tools/third-party/notion/)
      * [Tavily](../tools/third-party/tavily/)
      * [Agentic UI (AG-UI)](../tools/third-party/ag-ui/)
  + [Custom Tools](../tools-custom/)

    Custom Tools
    - Function tools




      Function tools
      * [Overview](../tools-custom/function-tools/)
      * [Tool performance](../tools-custom/performance/)
      * [Action confirmations](../tools-custom/confirmation/)
    - [MCP tools](../tools-custom/mcp-tools/)
    - [OpenAPI tools](../tools-custom/openapi-tools/)
    - [Authentication](../tools-custom/authentication/)
* Run Agents




  Run Agents
  + [Agent Runtime](../runtime/)

    Agent Runtime
    - [Runtime Config](../runtime/runconfig/)
    - [API Server](../runtime/api-server/)
    - [Resume Agents](../runtime/resume/)
  + [Deployment](../deploy/)

    Deployment
    - [Agent Engine](../deploy/agent-engine/)
    - [Cloud Run](../deploy/cloud-run/)
    - [GKE](../deploy/gke/)
  + Observability




    Observability
    - [Logging](../observability/logging/)
    - [Cloud Trace](../observability/cloud-trace/)
    - [AgentOps](../observability/agentops/)
    - [Arize AX](../observability/arize-ax/)
    - [Freeplay](../observability/freeplay/)
    - [Monocle](../observability/monocle/)
    - [Phoenix](../observability/phoenix/)
    - [W&B Weave](../observability/weave/)
  + [Evaluation](../evaluate/)

    Evaluation
    - [Criteria](../evaluate/criteria/)
    - [User Simulation](../evaluate/user-sim/)
  + [Safety and Security](../safety/)

    Safety and Security
* Components




  Components
  + [Technical Overview](../get-started/about/)
  + [Context](../context/)

    Context
    - [Context caching](../context/caching/)
    - [Context compression](../context/compaction/)
  + [Sessions & Memory](./)

    Sessions & Memory
    - [Session](session/)
    - [State](state/)
    - [Memory](memory/)
    - [Vertex AI Express Mode](express-mode/)
  + [Callbacks](../callbacks/)

    Callbacks
    - [Types of callbacks](../callbacks/types-of-callbacks/)
    - [Callback patterns](../callbacks/design-patterns-and-best-practices/)
  + [Artifacts](../artifacts/)

    Artifacts
  + [Events](../events/)

    Events
  + [Apps](../apps/)

    Apps
  + [Plugins](../plugins/)

    Plugins
    - [Reflect and retry](../plugins/reflect-and-retry/)
  + [MCP](../mcp/)

    MCP
  + [A2A Protocol](../a2a/)

    A2A Protocol
    - [Introduction to A2A](../a2a/intro/)
    - A2A Quickstart (Exposing)




      A2A Quickstart (Exposing)
      * [Python](../a2a/quickstart-exposing/)
      * [Go](../a2a/quickstart-exposing-go/)
    - A2A Quickstart (Consuming)




      A2A Quickstart (Consuming)
      * [Python](../a2a/quickstart-consuming/)
      * [Go](../a2a/quickstart-consuming-go/)
  + [Bidi-streaming (live)](../streaming/)

    Bidi-streaming (live)
    - [Custom Audio Bidi-streaming app sample (WebSockets)](../streaming/custom-streaming-ws/)
    - [Bidi-streaming development guide series](../streaming/dev-guide/part1/)
    - [Streaming Tools](../streaming/streaming-tools/)
    - [Configurating Bidi-streaming behaviour](../streaming/configuration/)
  + Grounding




    Grounding
    - [Understanding Google Search Grounding](../grounding/google_search_grounding/)
    - [Understanding Vertex AI Search Grounding](../grounding/vertex_ai_search_grounding/)
* Reference




  Reference
  + [API Reference](../api-reference/)

    API Reference
    - [Python ADK](../api-reference/python/)
    - [Go ADK](https://pkg.go.dev/google.golang.org/adk)
    - [Java ADK](../api-reference/java/)
    - [CLI Reference](../api-reference/cli/)
    - [Agent Config reference](../api-reference/agentconfig/)
    - [REST API](../api-reference/rest/)
  + [Community Resources](../community/)
  + [Contributing Guide](../contributing-guide/)

Table of contents

* [Core Concepts](#core-concepts)
* [Managing Context: Services](#managing-context-services)
* [What's Next?](#whats-next)

# Introduction to Conversational Context: Session, State, and Memory[¶](#introduction-to-conversational-context-session-state-and-memory "Permanent link")

Supported in ADKPythonGoJava

Meaningful, multi-turn conversations require agents to understand context. Just
like humans, they need to recall the conversation history: what's been said and
done to maintain continuity and avoid repetition. The Agent Development Kit
(ADK) provides structured ways to manage this context through `Session`,
`State`, and `Memory`.

## Core Concepts[¶](#core-concepts "Permanent link")

Think of different instances of your conversations with the agent as distinct
**conversation threads**, potentially drawing upon **long-term knowledge**.

1. **`Session`**: The Current Conversation Thread

   * Represents a *single, ongoing interaction* between a user and your agent
     system.
   * Contains the chronological sequence of messages and actions taken by the
     agent (referred to `Events`) during *that specific interaction*.
   * A `Session` can also hold temporary data (`State`) relevant only *during
     this conversation*.
2. **`State` (`session.state`)**: Data Within the Current Conversation

   * Data stored within a specific `Session`.
   * Used to manage information relevant *only* to the *current, active*
     conversation thread (e.g., items in a shopping cart *during this chat*,
     user preferences mentioned *in this session*).
3. **`Memory`**: Searchable, Cross-Session Information

   * Represents a store of information that might span *multiple past
     sessions* or include external data sources.
   * It acts as a knowledge base the agent can *search* to recall information
     or context beyond the immediate conversation.

## Managing Context: Services[¶](#managing-context-services "Permanent link")

ADK provides services to manage these concepts:

1. **`SessionService`**: Manages the different conversation threads (`Session`
   objects)

   * Handles the lifecycle: creating, retrieving, updating (appending
     `Events`, modifying `State`), and deleting individual `Session`s.
2. **`MemoryService`**: Manages the Long-Term Knowledge Store (`Memory`)

   * Handles ingesting information (often from completed `Session`s) into the
     long-term store.
   * Provides methods to search this stored knowledge based on queries.

**Implementations**: ADK offers different implementations for both
`SessionService` and `MemoryService`, allowing you to choose the storage backend
that best fits your application's needs. Notably, **in-memory implementations**
are provided for both services; these are designed specifically for **local
testing and fast development**. It's important to remember that **all data
stored using these in-memory options (sessions, state, or long-term knowledge)
is lost when your application restarts**. For persistence and scalability beyond
local testing, ADK also offers cloud-based and database service options.

**In Summary:**

* **`Session` & `State`**: Focus on the **current interaction** – the history
  and data of the *single, active conversation*. Managed primarily by a
  `SessionService`.
* **Memory**: Focuses on the **past and external information** – a *searchable
  archive* potentially spanning across conversations. Managed by a
  `MemoryService`.

## What's Next?[¶](#whats-next "Permanent link")

In the following sections, we'll dive deeper into each of these components:

* **`Session`**: Understanding its structure and `Events`.
* **`State`**: How to effectively read, write, and manage session-specific
  data.
* **`SessionService`**: Choosing the right storage backend for your sessions.
* **`MemoryService`**: Exploring options for storing and retrieving broader
  context.

Understanding these concepts is fundamental to building agents that can engage
in complex, stateful, and context-aware conversations.

Back to top