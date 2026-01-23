---
url: https://google.github.io/adk-docs/
source: Google ADK Documentation
---

[adk-python](https://github.com/google/adk-python "adk-python")

[adk-go](https://github.com/google/adk-go "adk-go")

[adk-java](https://github.com/google/adk-java "adk-java")

* [Home](.)

  Home
* Build Agents




  Build Agents
  + [Get Started](get-started/)

    Get Started
    - [Python](get-started/python/)
    - [Go](get-started/go/)
    - [Java](get-started/java/)
  + [Build your Agent](tutorials/)

    Build your Agent
    - [Multi-tool agent](get-started/quickstart/)
    - [Agent team](tutorials/agent-team/)
    - [Streaming agent](get-started/streaming/)

      Streaming agent
      * [Python](get-started/streaming/quickstart-streaming/)
      * [Java](get-started/streaming/quickstart-streaming-java/)
    - [Visual Builder](visual-builder/)
    - [Advanced setup](get-started/installation/)
  + [Agents](agents/)

    Agents
    - [LLM agents](agents/llm-agents/)
    - [Workflow agents](agents/workflow-agents/)

      Workflow agents
      * [Sequential agents](agents/workflow-agents/sequential-agents/)
      * [Loop agents](agents/workflow-agents/loop-agents/)
      * [Parallel agents](agents/workflow-agents/parallel-agents/)
    - [Custom agents](agents/custom-agents/)
    - [Multi-agent systems](agents/multi-agents/)
    - [Agent Config](agents/config/)
    - [Models & Authentication](agents/models/)
  + [Tools for Agents](tools/)

    Tools for Agents
    - [Built-in tools](tools/built-in-tools/)
    - Gemini API tools




      Gemini API tools
      * [Computer use](tools/gemini-api/computer-use/)
    - Google Cloud tools




      Google Cloud tools
      * [Overview](tools/google-cloud-tools/)
      * [MCP Toolbox for Databases](tools/google-cloud/mcp-toolbox-for-databases/)
      * [BigQuery Agent Analytics](tools/google-cloud/bigquery-agent-analytics/)
      * [Code Execution with Agent Engine](tools/google-cloud/code-exec-agent-engine/)
    - [Third-party tools](tools/third-party/)

      Third-party tools
      * [AgentQL](tools/third-party/agentql/)
      * [Bright Data](tools/third-party/bright-data/)
      * [Browserbase](tools/third-party/browserbase/)
      * [Exa](tools/third-party/exa/)
      * [Firecrawl](tools/third-party/firecrawl/)
      * [GitHub](tools/third-party/github/)
      * [Hugging Face](tools/third-party/hugging-face/)
      * [Notion](tools/third-party/notion/)
      * [Tavily](tools/third-party/tavily/)
      * [Agentic UI (AG-UI)](tools/third-party/ag-ui/)
  + [Custom Tools](tools-custom/)

    Custom Tools
    - Function tools




      Function tools
      * [Overview](tools-custom/function-tools/)
      * [Tool performance](tools-custom/performance/)
      * [Action confirmations](tools-custom/confirmation/)
    - [MCP tools](tools-custom/mcp-tools/)
    - [OpenAPI tools](tools-custom/openapi-tools/)
    - [Authentication](tools-custom/authentication/)
* Run Agents




  Run Agents
  + [Agent Runtime](runtime/)

    Agent Runtime
    - [Runtime Config](runtime/runconfig/)
    - [API Server](runtime/api-server/)
    - [Resume Agents](runtime/resume/)
  + [Deployment](deploy/)

    Deployment
    - [Agent Engine](deploy/agent-engine/)
    - [Cloud Run](deploy/cloud-run/)
    - [GKE](deploy/gke/)
  + Observability




    Observability
    - [Logging](observability/logging/)
    - [Cloud Trace](observability/cloud-trace/)
    - [AgentOps](observability/agentops/)
    - [Arize AX](observability/arize-ax/)
    - [Freeplay](observability/freeplay/)
    - [Monocle](observability/monocle/)
    - [Phoenix](observability/phoenix/)
    - [W&B Weave](observability/weave/)
  + [Evaluation](evaluate/)

    Evaluation
    - [Criteria](evaluate/criteria/)
    - [User Simulation](evaluate/user-sim/)
  + [Safety and Security](safety/)

    Safety and Security
* Components




  Components
  + [Technical Overview](get-started/about/)
  + [Context](context/)

    Context
    - [Context caching](context/caching/)
    - [Context compression](context/compaction/)
  + [Sessions & Memory](sessions/)

    Sessions & Memory
    - [Session](sessions/session/)
    - [State](sessions/state/)
    - [Memory](sessions/memory/)
    - [Vertex AI Express Mode](sessions/express-mode/)
  + [Callbacks](callbacks/)

    Callbacks
    - [Types of callbacks](callbacks/types-of-callbacks/)
    - [Callback patterns](callbacks/design-patterns-and-best-practices/)
  + [Artifacts](artifacts/)

    Artifacts
  + [Events](events/)

    Events
  + [Apps](apps/)

    Apps
  + [Plugins](plugins/)

    Plugins
    - [Reflect and retry](plugins/reflect-and-retry/)
  + [MCP](mcp/)

    MCP
  + [A2A Protocol](a2a/)

    A2A Protocol
    - [Introduction to A2A](a2a/intro/)
    - A2A Quickstart (Exposing)




      A2A Quickstart (Exposing)
      * [Python](a2a/quickstart-exposing/)
      * [Go](a2a/quickstart-exposing-go/)
    - A2A Quickstart (Consuming)




      A2A Quickstart (Consuming)
      * [Python](a2a/quickstart-consuming/)
      * [Go](a2a/quickstart-consuming-go/)
  + [Bidi-streaming (live)](streaming/)

    Bidi-streaming (live)
    - [Custom Audio Bidi-streaming app sample (WebSockets)](streaming/custom-streaming-ws/)
    - [Bidi-streaming development guide series](streaming/dev-guide/part1/)
    - [Streaming Tools](streaming/streaming-tools/)
    - [Configurating Bidi-streaming behaviour](streaming/configuration/)
  + Grounding




    Grounding
    - [Understanding Google Search Grounding](grounding/google_search_grounding/)
    - [Understanding Vertex AI Search Grounding](grounding/vertex_ai_search_grounding/)
* Reference




  Reference
  + [API Reference](api-reference/)

    API Reference
    - [Python ADK](api-reference/python/)
    - [Go ADK](https://pkg.go.dev/google.golang.org/adk)
    - [Java ADK](api-reference/java/)
    - [CLI Reference](api-reference/cli/)
    - [Agent Config reference](api-reference/agentconfig/)
    - [REST API](api-reference/rest/)
  + [Community Resources](community/)
  + [Contributing Guide](contributing-guide/)

Table of contents

* [Learn more](#learn-more)

![Agent Development Kit Logo](assets/agent-development-kit.png)

# Agent Development Kit

Agent Development Kit (ADK) is a flexible and modular framework for **developing
and deploying AI agents**. While optimized for Gemini and the Google ecosystem,
ADK is **model-agnostic**, **deployment-agnostic**, and is built for
**compatibility with other frameworks**. ADK was designed to make agent
development feel more like software development, to make it easier for
developers to create, deploy, and orchestrate agentic architectures that range
from simple tasks to complex workflows.

Get started:

PythonGoJava

`pip install google-adk`

`go get google.golang.org/adk`

pom.xml

```python
<dependency>
    <groupId>com.google.adk</groupId>
    <artifactId>google-adk</artifactId>
    <version>0.3.0</version>
</dependency>
```

build.gradle

```python
dependencies {
    implementation 'com.google.adk:google-adk:0.3.0'
}
```

[Start with Python](/adk-docs/get-started/python/)
[Start with Go](/adk-docs/get-started/go/)
[Start with Java](/adk-docs/get-started/java/)

---

## Learn more[¶](#learn-more "Permanent link")

[Watch "Introducing Agent Development Kit"!](https://www.youtube.com/watch?v=zgrOwow_uTQ)

* **Flexible Orchestration**

  ---

  Define workflows using workflow agents (`Sequential`, `Parallel`, `Loop`)
  for predictable pipelines, or leverage LLM-driven dynamic routing
  (`LlmAgent` transfer) for adaptive behavior.

  [**Learn about agents**](agents/)
* **Multi-Agent Architecture**

  ---

  Build modular and scalable applications by composing multiple specialized
  agents in a hierarchy. Enable complex coordination and delegation.

  [**Explore multi-agent systems**](agents/multi-agents/)
* **Rich Tool Ecosystem**

  ---

  Equip agents with diverse capabilities: use pre-built tools (Search, Code
  Exec), create custom functions, integrate 3rd-party libraries, or even use
  other agents as tools.

  [**Browse tools**](tools/)
* **Deployment Ready**

  ---

  Containerize and deploy your agents anywhere – run locally, scale with
  Vertex AI Agent Engine, or integrate into custom infrastructure using Cloud
  Run or Docker.

  [**Deploy agents**](deploy/)
* **Built-in Evaluation**

  ---

  Systematically assess agent performance by evaluating both the final
  response quality and the step-by-step execution trajectory against
  predefined test cases.

  [**Evaluate agents**](evaluate/)
* **Building Safe and Secure Agents**

  ---

  Learn how to building powerful and trustworthy agents by implementing
  security and safety patterns and best practices into your agent's design.

  [**Safety and Security**](safety/)

Back to top