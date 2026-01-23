---
url: https://google.github.io/adk-docs/agents/workflow-agents/
source: Google ADK Documentation
---

[adk-python](https://github.com/google/adk-python "adk-python")

[adk-go](https://github.com/google/adk-go "adk-go")

[adk-java](https://github.com/google/adk-java "adk-java")

* [Home](../..)

  Home
* Build Agents




  Build Agents
  + [Get Started](../../get-started/)

    Get Started
    - [Python](../../get-started/python/)
    - [Go](../../get-started/go/)
    - [Java](../../get-started/java/)
  + [Build your Agent](../../tutorials/)

    Build your Agent
    - [Multi-tool agent](../../get-started/quickstart/)
    - [Agent team](../../tutorials/agent-team/)
    - [Streaming agent](../../get-started/streaming/)

      Streaming agent
      * [Python](../../get-started/streaming/quickstart-streaming/)
      * [Java](../../get-started/streaming/quickstart-streaming-java/)
    - [Visual Builder](../../visual-builder/)
    - [Advanced setup](../../get-started/installation/)
  + [Agents](../)

    Agents
    - [LLM agents](../llm-agents/)
    - [Workflow agents](./)

      Workflow agents
      * [Sequential agents](sequential-agents/)
      * [Loop agents](loop-agents/)
      * [Parallel agents](parallel-agents/)
    - [Custom agents](../custom-agents/)
    - [Multi-agent systems](../multi-agents/)
    - [Agent Config](../config/)
    - [Models & Authentication](../models/)
  + [Tools for Agents](../../tools/)

    Tools for Agents
    - [Built-in tools](../../tools/built-in-tools/)
    - Gemini API tools




      Gemini API tools
      * [Computer use](../../tools/gemini-api/computer-use/)
    - Google Cloud tools




      Google Cloud tools
      * [Overview](../../tools/google-cloud-tools/)
      * [MCP Toolbox for Databases](../../tools/google-cloud/mcp-toolbox-for-databases/)
      * [BigQuery Agent Analytics](../../tools/google-cloud/bigquery-agent-analytics/)
      * [Code Execution with Agent Engine](../../tools/google-cloud/code-exec-agent-engine/)
    - [Third-party tools](../../tools/third-party/)

      Third-party tools
      * [AgentQL](../../tools/third-party/agentql/)
      * [Bright Data](../../tools/third-party/bright-data/)
      * [Browserbase](../../tools/third-party/browserbase/)
      * [Exa](../../tools/third-party/exa/)
      * [Firecrawl](../../tools/third-party/firecrawl/)
      * [GitHub](../../tools/third-party/github/)
      * [Hugging Face](../../tools/third-party/hugging-face/)
      * [Notion](../../tools/third-party/notion/)
      * [Tavily](../../tools/third-party/tavily/)
      * [Agentic UI (AG-UI)](../../tools/third-party/ag-ui/)
  + [Custom Tools](../../tools-custom/)

    Custom Tools
    - Function tools




      Function tools
      * [Overview](../../tools-custom/function-tools/)
      * [Tool performance](../../tools-custom/performance/)
      * [Action confirmations](../../tools-custom/confirmation/)
    - [MCP tools](../../tools-custom/mcp-tools/)
    - [OpenAPI tools](../../tools-custom/openapi-tools/)
    - [Authentication](../../tools-custom/authentication/)
* Run Agents




  Run Agents
  + [Agent Runtime](../../runtime/)

    Agent Runtime
    - [Runtime Config](../../runtime/runconfig/)
    - [API Server](../../runtime/api-server/)
    - [Resume Agents](../../runtime/resume/)
  + [Deployment](../../deploy/)

    Deployment
    - [Agent Engine](../../deploy/agent-engine/)
    - [Cloud Run](../../deploy/cloud-run/)
    - [GKE](../../deploy/gke/)
  + Observability




    Observability
    - [Logging](../../observability/logging/)
    - [Cloud Trace](../../observability/cloud-trace/)
    - [AgentOps](../../observability/agentops/)
    - [Arize AX](../../observability/arize-ax/)
    - [Freeplay](../../observability/freeplay/)
    - [Monocle](../../observability/monocle/)
    - [Phoenix](../../observability/phoenix/)
    - [W&B Weave](../../observability/weave/)
  + [Evaluation](../../evaluate/)

    Evaluation
    - [Criteria](../../evaluate/criteria/)
    - [User Simulation](../../evaluate/user-sim/)
  + [Safety and Security](../../safety/)

    Safety and Security
* Components




  Components
  + [Technical Overview](../../get-started/about/)
  + [Context](../../context/)

    Context
    - [Context caching](../../context/caching/)
    - [Context compression](../../context/compaction/)
  + [Sessions & Memory](../../sessions/)

    Sessions & Memory
    - [Session](../../sessions/session/)
    - [State](../../sessions/state/)
    - [Memory](../../sessions/memory/)
    - [Vertex AI Express Mode](../../sessions/express-mode/)
  + [Callbacks](../../callbacks/)

    Callbacks
    - [Types of callbacks](../../callbacks/types-of-callbacks/)
    - [Callback patterns](../../callbacks/design-patterns-and-best-practices/)
  + [Artifacts](../../artifacts/)

    Artifacts
  + [Events](../../events/)

    Events
  + [Apps](../../apps/)

    Apps
  + [Plugins](../../plugins/)

    Plugins
    - [Reflect and retry](../../plugins/reflect-and-retry/)
  + [MCP](../../mcp/)

    MCP
  + [A2A Protocol](../../a2a/)

    A2A Protocol
    - [Introduction to A2A](../../a2a/intro/)
    - A2A Quickstart (Exposing)




      A2A Quickstart (Exposing)
      * [Python](../../a2a/quickstart-exposing/)
      * [Go](../../a2a/quickstart-exposing-go/)
    - A2A Quickstart (Consuming)




      A2A Quickstart (Consuming)
      * [Python](../../a2a/quickstart-consuming/)
      * [Go](../../a2a/quickstart-consuming-go/)
  + [Bidi-streaming (live)](../../streaming/)

    Bidi-streaming (live)
    - [Custom Audio Bidi-streaming app sample (WebSockets)](../../streaming/custom-streaming-ws/)
    - [Bidi-streaming development guide series](../../streaming/dev-guide/part1/)
    - [Streaming Tools](../../streaming/streaming-tools/)
    - [Configurating Bidi-streaming behaviour](../../streaming/configuration/)
  + Grounding




    Grounding
    - [Understanding Google Search Grounding](../../grounding/google_search_grounding/)
    - [Understanding Vertex AI Search Grounding](../../grounding/vertex_ai_search_grounding/)
* Reference




  Reference
  + [API Reference](../../api-reference/)

    API Reference
    - [Python ADK](../../api-reference/python/)
    - [Go ADK](https://pkg.go.dev/google.golang.org/adk)
    - [Java ADK](../../api-reference/java/)
    - [CLI Reference](../../api-reference/cli/)
    - [Agent Config reference](../../api-reference/agentconfig/)
    - [REST API](../../api-reference/rest/)
  + [Community Resources](../../community/)
  + [Contributing Guide](../../contributing-guide/)

Table of contents

* [Why Use Workflow Agents?](#why-use-workflow-agents)

# Workflow Agents[¶](#workflow-agents "Permanent link")

Supported in ADKPythonGoJava

This section introduces "*workflow agents*" - **specialized agents that control the execution flow of its sub-agents**.

Workflow agents are specialized components in ADK designed purely for **orchestrating the execution flow of sub-agents**. Their primary role is to manage *how* and *when* other agents run, defining the control flow of a process.

Unlike [LLM Agents](../llm-agents/), which use Large Language Models for dynamic reasoning and decision-making, Workflow Agents operate based on **predefined logic**. They determine the execution sequence according to their type (e.g., sequential, parallel, loop) without consulting an LLM for the orchestration itself. This results in **deterministic and predictable execution patterns**.

ADK provides three core workflow agent types, each implementing a distinct execution pattern:

* **Sequential Agents**

  ---

  Executes sub-agents one after another, in **sequence**.

  [Learn more](sequential-agents/)
* **Loop Agents**

  ---

  **Repeatedly** executes its sub-agents until a specific termination condition is met.

  [Learn more](loop-agents/)
* **Parallel Agents**

  ---

  Executes multiple sub-agents in **parallel**.

  [Learn more](parallel-agents/)

## Why Use Workflow Agents?[¶](#why-use-workflow-agents "Permanent link")

Workflow agents are essential when you need explicit control over how a series of tasks or agents are executed. They provide:

* **Predictability:** The flow of execution is guaranteed based on the agent type and configuration.
* **Reliability:** Ensures tasks run in the required order or pattern consistently.
* **Structure:** Allows you to build complex processes by composing agents within clear control structures.

While the workflow agent manages the control flow deterministically, the sub-agents it orchestrates can themselves be any type of agent, including intelligent LLM Agent instances. This allows you to combine structured process control with flexible, LLM-powered task execution.

Back to top