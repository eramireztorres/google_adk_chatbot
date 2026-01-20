---
url: https://google.github.io/adk-docs/streaming/
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
  + [Bidi-streaming (live)](./)

    Bidi-streaming (live)
    - [Custom Audio Bidi-streaming app sample (WebSockets)](custom-streaming-ws/)
    - [Bidi-streaming development guide series](dev-guide/part1/)
    - [Streaming Tools](streaming-tools/)
    - [Configurating Bidi-streaming behaviour](configuration/)
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

# Bidi-streaming (live) in ADK[¶](#bidi-streaming-live-in-adk "Permanent link")

Supported in ADKPython v0.5.0Experimental

Bidirectional (Bidi) streaming (live) in ADK adds the low-latency bidirectional voice and video interaction
capability of [Gemini Live API](https://ai.google.dev/gemini-api/docs/live) to
AI agents.

Experimental preview release

The Bidirectional (Bidi) streaming feature is experimental.

With bidi-streaming, or live, mode, you can provide end users with the experience of natural,
human-like voice conversations, including the ability for the user to interrupt
the agent's responses with voice commands. Agents with streaming can process
text, audio, and video inputs, and they can provide text and audio output.

Info

This is different from server-side streaming or token-level streaming.
Token-level streaming is a one-way process where a language model generates a response and sends it back to the user one token at a time. This creates a "typing" effect, giving the impression of an immediate response and reducing the time it takes to see the start of the answer. The user sends their full prompt, the model processes it, and then the model begins to generate and send back the response piece by piece. This section is for bidi-streaming (live).

* **Quickstart (Bidi-streaming)**

  ---

  In this quickstart, you'll build a simple agent and use streaming in ADK to
  implement low-latency and bidirectional voice and video communication.

  + [Quickstart (Bidi-streaming)](../get-started/streaming/quickstart-streaming/)
* **Custom Audio Streaming app sample**

  ---

  This article overviews the server and client code for a custom asynchronous web app built with ADK Streaming and FastAPI, enabling real-time, bidirectional audio and text communication with WebSockets.

  + [Custom Audio Streaming app sample (WebSockets)](custom-streaming-ws/)
* **Bidi-streaming development guide series**

  ---

  A series of articles for diving deeper into the Bidi-streaming development with ADK. You can learn basic concepts and use cases, the core API, and end-to-end application design.

  + [Bidi-streaming development guide series: Part 1 - Introduction](dev-guide/part1/)
* **Streaming Tools**

  ---

  Streaming tools allows tools (functions) to stream intermediate results back to agents and agents can respond to those intermediate results. For example, we can use streaming tools to monitor the changes of the stock price and have the agent react to it. Another example is we can have the agent monitor the video stream, and when there is changes in video stream, the agent can report the changes.

  + [Streaming Tools](streaming-tools/)
* **Custom Audio Streaming app sample**

  ---

  This article overviews the server and client code for a custom asynchronous web app built with ADK Streaming and FastAPI, enabling real-time, bidirectional audio and text communication with both Server Sent Events (SSE) and WebSockets.

  + [Streaming Configurations](configuration/)
* **Blog post: Google ADK + Vertex AI Live API**

  ---

  This article shows how to use Bidi-streaming (live) in ADK for real-time audio/video streaming. It offers a Python server example using LiveRequestQueue to build custom, interactive AI agents.

  + [Blog post: Google ADK + Vertex AI Live API](https://medium.com/google-cloud/google-adk-vertex-ai-live-api-125238982d5e)
* **Blog post: Supercharge ADK Development with Claude Code Skills**

  ---

  This article demonstrates how to use Claude Code Skills to accelerate ADK development, with an example of building a Bidi-streaming chat app. Learn how to leverage AI-powered coding assistance to build better agents faster.

  + [Blog post: Supercharge ADK Development with Claude Code Skills](https://medium.com/@kazunori279/supercharge-adk-development-with-claude-code-skills-d192481cbe72)

Back to top