---
url: https://google.github.io/adk-docs/agents/
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
  + [Agents](./)

    Agents
    - [LLM agents](llm-agents/)
    - [Workflow agents](workflow-agents/)

      Workflow agents
      * [Sequential agents](workflow-agents/sequential-agents/)
      * [Loop agents](workflow-agents/loop-agents/)
      * [Parallel agents](workflow-agents/parallel-agents/)
    - [Custom agents](custom-agents/)
    - [Multi-agent systems](multi-agents/)
    - [Agent Config](config/)
    - [Models & Authentication](models/)
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

* [Core Agent Categories](#core-agent-categories)
* [Choosing the Right Agent Type](#choosing-the-right-agent-type)
* [Agents Working Together: Multi-Agent Systems](#agents-working-together-multi-agent-systems)
* [What's Next?](#whats-next)

# Agents[¶](#agents "Permanent link")

Supported in ADKPythonGoJava

In the Agent Development Kit (ADK), an **Agent** is a self-contained execution unit designed to act autonomously to achieve specific goals. Agents can perform tasks, interact with users, utilize external tools, and coordinate with other agents.

The foundation for all agents in ADK is the `BaseAgent` class. It serves as the fundamental blueprint. To create functional agents, you typically extend `BaseAgent` in one of three main ways, catering to different needs – from intelligent reasoning to structured process control.

![Types of agents in ADK](../assets/agent-types.png)

## Core Agent Categories[¶](#core-agent-categories "Permanent link")

ADK provides distinct agent categories to build sophisticated applications:

1. [**LLM Agents (`LlmAgent`, `Agent`)**](llm-agents/): These agents utilize Large Language Models (LLMs) as their core engine to understand natural language, reason, plan, generate responses, and dynamically decide how to proceed or which tools to use, making them ideal for flexible, language-centric tasks. [Learn more about LLM Agents...](llm-agents/)
2. [**Workflow Agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`)**](workflow-agents/): These specialized agents control the execution flow of other agents in predefined, deterministic patterns (sequence, parallel, or loop) without using an LLM for the flow control itself, perfect for structured processes needing predictable execution. [Explore Workflow Agents...](workflow-agents/)
3. [**Custom Agents**](custom-agents/): Created by extending `BaseAgent` directly, these agents allow you to implement unique operational logic, specific control flows, or specialized integrations not covered by the standard types, catering to highly tailored application requirements. [Discover how to build Custom Agents...](custom-agents/)

## Choosing the Right Agent Type[¶](#choosing-the-right-agent-type "Permanent link")

The following table provides a high-level comparison to help distinguish between the agent types. As you explore each type in more detail in the subsequent sections, these distinctions will become clearer.

| Feature | LLM Agent (`LlmAgent`) | Workflow Agent | Custom Agent (`BaseAgent` subclass) |
| --- | --- | --- | --- |
| **Primary Function** | Reasoning, Generation, Tool Use | Controlling Agent Execution Flow | Implementing Unique Logic/Integrations |
| **Core Engine** | Large Language Model (LLM) | Predefined Logic (Sequence, Parallel, Loop) | Custom Code |
| **Determinism** | Non-deterministic (Flexible) | Deterministic (Predictable) | Can be either, based on implementation |
| **Primary Use** | Language tasks, Dynamic decisions | Structured processes, Orchestration | Tailored requirements, Specific workflows |

## Agents Working Together: Multi-Agent Systems[¶](#agents-working-together-multi-agent-systems "Permanent link")

While each agent type serves a distinct purpose, the true power often comes from combining them. Complex applications frequently employ [multi-agent architectures](multi-agents/) where:

* **LLM Agents** handle intelligent, language-based task execution.
* **Workflow Agents** manage the overall process flow using standard patterns.
* **Custom Agents** provide specialized capabilities or rules needed for unique integrations.

Understanding these core types is the first step toward building sophisticated, capable AI applications with ADK.

---

## What's Next?[¶](#whats-next "Permanent link")

Now that you have an overview of the different agent types available in ADK, dive deeper into how they work and how to use them effectively:

* [**LLM Agents:**](llm-agents/) Explore how to configure agents powered by large language models, including setting instructions, providing tools, and enabling advanced features like planning and code execution.
* [**Workflow Agents:**](workflow-agents/) Learn how to orchestrate tasks using `SequentialAgent`, `ParallelAgent`, and `LoopAgent` for structured and predictable processes.
* [**Custom Agents:**](custom-agents/) Discover the principles of extending `BaseAgent` to build agents with unique logic and integrations tailored to your specific needs.
* [**Multi-Agents:**](multi-agents/) Understand how to combine different agent types to create sophisticated, collaborative systems capable of tackling complex problems.
* [**Models:**](models/) Learn about the different LLM integrations available and how to select the right model for your agents.

Back to top