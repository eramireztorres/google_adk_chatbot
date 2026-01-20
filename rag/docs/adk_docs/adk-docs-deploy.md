---
url: https://google.github.io/adk-docs/deploy/
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
  + [Deployment](./)

    Deployment
    - [Agent Engine](agent-engine/)
    - [Cloud Run](cloud-run/)
    - [GKE](gke/)
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

* [Deployment Options](#deployment-options)

  + [Agent Engine in Vertex AI](#agent-engine-in-vertex-ai)
  + [Cloud Run](#cloud-run)
  + [Google Kubernetes Engine (GKE)](#google-kubernetes-engine-gke)
  + [Other Container-friendly Infrastructure](#other-container-friendly-infrastructure)

# Deploying Your Agent[¶](#deploying-your-agent "Permanent link")

Once you've built and tested your agent using ADK,
the next step is to deploy it so it can be accessed, queried, and used in
production or integrated with other applications. Deployment moves your agent
from your local development machine to a scalable and reliable environment.

![Deploying your agent](../assets/deploy-agent.png)

## Deployment Options[¶](#deployment-options "Permanent link")

Your ADK agent can be deployed to a range of different environments based
on your needs for production readiness or custom flexibility:

### Agent Engine in Vertex AI[¶](#agent-engine-in-vertex-ai "Permanent link")

[Agent Engine](agent-engine/) is a fully managed auto-scaling service on Google Cloud
specifically designed for deploying, managing, and scaling AI agents built with
frameworks such as ADK.

Learn more about [deploying your agent to Vertex AI Agent Engine](agent-engine/).

### Cloud Run[¶](#cloud-run "Permanent link")

[Cloud Run](https://cloud.google.com/run) is a managed auto-scaling compute platform on
Google Cloud that enables you to run your agent as a container-based
application.

Learn more about [deploying your agent to Cloud Run](cloud-run/).

### Google Kubernetes Engine (GKE)[¶](#google-kubernetes-engine-gke "Permanent link")

[Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine) is a managed
Kubernetes service of Google Cloud that allows you to run your agent in a containerized
environment. GKE is a good option if you need more control over the deployment as well as
for running Open Models.

Learn more about [deploying your agent to GKE](gke/).

### Other Container-friendly Infrastructure[¶](#other-container-friendly-infrastructure "Permanent link")

You can manually package your Agent into a container image and then run it in
any environment that supports container images. For example you can run it
locally in Docker or Podman. This is a good option if you prefer to run offline
or disconnected, or otherwise in a system that has no connection to Google
Cloud.

Follow the instructions for [deploying your agent to Cloud Run](cloud-run/#deployment-commands).
In the "Deployment Commands" section for gcloud CLI, you will find an example FastAPI entry point and
Dockerfile.

Back to top