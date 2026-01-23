---
url: https://google.github.io/adk-docs/api-reference/
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
  + [API Reference](./)

    API Reference
    - [Python ADK](python/)
    - [Go ADK](https://pkg.go.dev/google.golang.org/adk)
    - [Java ADK](java/)
    - [CLI Reference](cli/)
    - [Agent Config reference](agentconfig/)
    - [REST API](rest/)
  + [Community Resources](../community/)
  + [Contributing Guide](../contributing-guide/)

# API Reference[¶](#api-reference "Permanent link")

The Agent Development Kit (ADK) provides comprehensive API references for both Python and Java, allowing you to dive deep into all available classes, methods, and functionalities.

* **Python API Reference**

  ---

  Explore the complete API documentation for the Python Agent Development Kit. Discover detailed information on all modules, classes, functions, and examples to build sophisticated AI agents with Python.

  [View Python API Docs](python/)

* **Go API Reference**

  ---

  Explore the complete API documentation for the Go Agent Development Kit. Discover detailed information on all modules, classes, and functions to build sophisticated AI agents with Go.

  [View Go API Docs](https://pkg.go.dev/google.golang.org/adk)

* **Java API Reference**

  ---

  Access the comprehensive Javadoc for the Java Agent Development Kit. This reference provides detailed specifications for all packages, classes, interfaces, and methods, enabling you to develop robust AI agents using Java.

  [View Java API Docs](java/)

* **CLI Reference**

  ---

  Explore the complete API documentation for the CLI including all of the
  valid options and subcommands.

  [View CLI Docs](cli/)

* **Agent Config YAML reference**

  ---

  View the full Agent Config syntax for configuring ADK with
  YAML text files.

  [View Agent Config reference](agentconfig/)

* **REST API Reference**

  ---

  Explore the REST API for the ADK web server. This reference provides details on the available endpoints, request and response formats, and more.

  [View REST API Docs](rest/)

Back to top