---
url: https://google.github.io/adk-docs/a2a/
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
  + [Sessions & Memory](../sessions/)

    Sessions & Memory
    - [Session](../sessions/session/)
    - [State](../sessions/state/)
    - [Memory](../sessions/memory/)
    - [Vertex AI Express Mode](../sessions/express-mode/)
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
  + [A2A Protocol](./)

    A2A Protocol
    - [Introduction to A2A](intro/)
    - A2A Quickstart (Exposing)




      A2A Quickstart (Exposing)
      * [Python](quickstart-exposing/)
      * [Go](quickstart-exposing-go/)
    - A2A Quickstart (Consuming)




      A2A Quickstart (Consuming)
      * [Python](quickstart-consuming/)
      * [Go](quickstart-consuming-go/)
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

# ADK with Agent2Agent (A2A) Protocol[¶](#adk-with-agent2agent-a2a-protocol "Permanent link")

Supported in ADKPythonGoExperimental

With Agent Development Kit (ADK), you can build complex multi-agent systems where different agents need to collaborate and interact using [Agent2Agent (A2A) Protocol](https://a2a-protocol.org/)! This section provides a comprehensive guide to building powerful multi-agent systems where agents can communicate and collaborate securely and efficiently.

Navigate through the guides below to learn about ADK's A2A capabilities:

**[Introduction to A2A](intro/)**

Start here to learn the fundamentals of A2A by building a multi-agent system with a root agent, a local sub-agent, and a remote A2A agent. The following guides cover how do I expose your agent so that other agents can use it via the A2A protocol:

* **[A2A Quickstart (Exposing) for Python](quickstart-exposing/)**
* **[A2A Quickstart (Exposing) for Go](quickstart-exposing-go/)**

These guides show you how to allow your agent to use another, remote agent using A2A protocol:

* **[A2A Quickstart (Consuming) for Python](quickstart-consuming/)**
* **[A2A Quickstart (Consuming) for Go](quickstart-consuming-go/)**

[**Official Website for Agent2Agent (A2A) Protocol**](https://a2a-protocol.org/)

The official website for A2A Protocol.

Back to top