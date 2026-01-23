---
url: https://google.github.io/adk-docs/a2a/quickstart-exposing-go/
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
  + [Agents](../../agents/)

    Agents
    - [LLM agents](../../agents/llm-agents/)
    - [Workflow agents](../../agents/workflow-agents/)

      Workflow agents
      * [Sequential agents](../../agents/workflow-agents/sequential-agents/)
      * [Loop agents](../../agents/workflow-agents/loop-agents/)
      * [Parallel agents](../../agents/workflow-agents/parallel-agents/)
    - [Custom agents](../../agents/custom-agents/)
    - [Multi-agent systems](../../agents/multi-agents/)
    - [Agent Config](../../agents/config/)
    - [Models & Authentication](../../agents/models/)
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
  + [A2A Protocol](../)

    A2A Protocol
    - [Introduction to A2A](../intro/)
    - A2A Quickstart (Exposing)




      A2A Quickstart (Exposing)
      * [Python](../quickstart-exposing/)
      * Go

        [Go](./)



        Table of contents
        + [Overview](#overview)
        + [Exposing the Remote Agent with the A2A Launcher](#exposing-the-remote-agent-with-the-a2a-launcher)

          - [1. Getting the Sample Code](#getting-the-sample-code)

            * [Root Agent (a2a\_basic/main.go)](#root-agent-a2a_basicmaingo)
            * [Remote Prime Agent (a2a\_basic/remote\_a2a/check\_prime\_agent/main.go)](#remote-prime-agent-a2a_basicremote_a2acheck_prime_agentmaingo)
          - [2. Start the Remote A2A Agent server](#start-the-remote-a2a-agent-server)
          - [3. Check that your remote agent is running](#check-that-your-remote-agent-is-running)
          - [4. Run the Main (Consuming) Agent](#run-the-main-consuming-agent)

            * [How it works](#how-it-works)
        + [Example Interactions](#example-interactions)
        + [Next Steps](#next-steps)
    - A2A Quickstart (Consuming)




      A2A Quickstart (Consuming)
      * [Python](../quickstart-consuming/)
      * [Go](../quickstart-consuming-go/)
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

* [Overview](#overview)
* [Exposing the Remote Agent with the A2A Launcher](#exposing-the-remote-agent-with-the-a2a-launcher)

  + [1. Getting the Sample Code](#getting-the-sample-code)

    - [Root Agent (a2a\_basic/main.go)](#root-agent-a2a_basicmaingo)
    - [Remote Prime Agent (a2a\_basic/remote\_a2a/check\_prime\_agent/main.go)](#remote-prime-agent-a2a_basicremote_a2acheck_prime_agentmaingo)
  + [2. Start the Remote A2A Agent server](#start-the-remote-a2a-agent-server)
  + [3. Check that your remote agent is running](#check-that-your-remote-agent-is-running)
  + [4. Run the Main (Consuming) Agent](#run-the-main-consuming-agent)

    - [How it works](#how-it-works)
* [Example Interactions](#example-interactions)
* [Next Steps](#next-steps)

# Quickstart: Exposing a remote agent via A2A[¶](#quickstart-exposing-a-remote-agent-via-a2a "Permanent link")

Supported in ADKGoExperimental

This quickstart covers the most common starting point for any developer: **"I have an agent. How do I expose it so that other agents can use my agent via A2A?"**. This is crucial for building complex multi-agent systems where different agents need to collaborate and interact.

## Overview[¶](#overview "Permanent link")

This sample demonstrates how you can easily expose an ADK agent so that it can be then consumed by another agent using the A2A Protocol.

In Go, you expose an agent by using the A2A launcher, which dynamically generates an agent card for you.

```python
┌─────────────────┐                             ┌───────────────────────────────┐
│   Root Agent    │       A2A Protocol          │ A2A-Exposed Check Prime Agent │
│                 │────────────────────────────▶│      (localhost: 8001)        │
└─────────────────┘                             └───────────────────────────────┘
```

The sample consists of :

* **Remote Prime Agent** (`remote_a2a/check_prime_agent/main.go`): This is the agent that you want to expose so that other agents can use it via A2A. It is an agent that handles prime number checking. It becomes exposed using the A2A launcher.
* **Root Agent** (`main.go`): A simple agent that is just calling the remote prime agent.

## Exposing the Remote Agent with the A2A Launcher[¶](#exposing-the-remote-agent-with-the-a2a-launcher "Permanent link")

You can take an existing agent built using the Go ADK and make it A2A-compatible by using the A2A launcher.

### 1. Getting the Sample Code[¶](#getting-the-sample-code "Permanent link")

First, make sure you have Go installed and your environment is set up.

You can clone and navigate to the [**`a2a_basic`** sample](https://github.com/google/adk-docs/tree/main/examples/go/a2a_basic) here:

```python
cd examples/go/a2a_basic
```

As you'll see, the folder structure is as follows:

```python
a2a_basic/
├── remote_a2a/
│   └── check_prime_agent/
│       └── main.go    # Remote Prime Agent
├── go.mod
├── go.sum
└── main.go            # Root agent
```

#### Root Agent (`a2a_basic/main.go`)[¶](#root-agent-a2a_basicmaingo "Permanent link")

* **`newRootAgent`**: A local agent that connects to the remote A2A service.

#### Remote Prime Agent (`a2a_basic/remote_a2a/check_prime_agent/main.go`)[¶](#remote-prime-agent-a2a_basicremote_a2acheck_prime_agentmaingo "Permanent link")

* **`checkPrimeTool`**: Function for prime number checking.
* **`main`**: The main function that creates the agent and starts the A2A server.

### 2. Start the Remote A2A Agent server[¶](#start-the-remote-a2a-agent-server "Permanent link")

You can now start the remote agent server, which will host the `check_prime_agent`:

```python
# Start the remote agent
go run remote_a2a/check_prime_agent/main.go
```

Once executed, you should see something like:

```python
2025/11/06 11:00:19 Starting A2A prime checker server on port 8001
2025/11/06 11:00:19 Starting the web server: &{port:8001}
2025/11/06 11:00:19 
2025/11/06 11:00:19 Web servers starts on http://localhost:8001
2025/11/06 11:00:19        a2a:  you can access A2A using jsonrpc protocol: http://localhost:8001
```

### 3. Check that your remote agent is running[¶](#check-that-your-remote-agent-is-running "Permanent link")

You can check that your agent is up and running by visiting the agent card that was auto-generated by the A2A launcher:

<http://localhost:8001/.well-known/agent-card.json>

You should see the contents of the agent card.

### 4. Run the Main (Consuming) Agent[¶](#run-the-main-consuming-agent "Permanent link")

Now that your remote agent is running, you can run the main agent.

```python
# In a separate terminal, run the main agent
go run main.go
```

#### How it works[¶](#how-it-works "Permanent link")

The remote agent is exposed using the A2A launcher in the `main` function. The launcher takes care of starting the server and generating the agent card.

remote\_a2a/check\_prime\_agent/main.go

```python
func main() {
    ctx := context.Background()
    primeTool, err := functiontool.New(functiontool.Config{
        Name:        "prime_checking",
        Description: "Check if numbers in a list are prime using efficient mathematical algorithms",
    }, checkPrimeTool)
    if err != nil {
        log.Fatalf("Failed to create prime_checking tool: %v", err)
    }

    model, err := gemini.NewModel(ctx, "gemini-2.0-flash", &genai.ClientConfig{})
    if err != nil {
        log.Fatalf("Failed to create model: %v", err)
    }

    primeAgent, err := llmagent.New(llmagent.Config{
        Name:        "check_prime_agent",
        Description: "check prime agent that can check whether numbers are prime.",
        Instruction: `
            You check whether numbers are prime.
            When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
            You should not rely on the previous history on prime results.
    `,
        Model: model,
        Tools: []tool.Tool{primeTool},
    })
    if err != nil {
        log.Fatalf("Failed to create agent: %v", err)
    }

    // Create launcher. The a2a.NewLauncher() will dynamically generate the agent card.
    port := 8001
    launcher := web.NewLauncher(a2a.NewLauncher())
    _, err = launcher.Parse([]string{
        "--port", strconv.Itoa(port),
        "a2a", "--a2a_agent_url", "http://localhost:" + strconv.Itoa(port),
    })
    if err != nil {
        log.Fatalf("launcher.Parse() error = %v", err)
    }

    // Create ADK config
    config := &adk.Config{
        AgentLoader:    services.NewSingleAgentLoader(primeAgent),
        SessionService: session.InMemoryService(),
    }

    log.Printf("Starting A2A prime checker server on port %d\n", port)
    // Run launcher
    if err := launcher.Run(context.Background(), config); err != nil {
        log.Fatalf("launcher.Run() error = %v", err)
    }
}
```

## Example Interactions[¶](#example-interactions "Permanent link")

Once both services are running, you can interact with the root agent to see how it calls the remote agent via A2A:

**Prime Number Checking:**

This interaction uses a remote agent via A2A, the Prime Agent:

```python
User: roll a die and check if it's a prime
Bot: Okay, I will first roll a die and then check if the result is a prime number.

Bot calls tool: transfer_to_agent with args: map[agent_name:roll_agent]
Bot calls tool: roll_die with args: map[sides:6]
Bot calls tool: transfer_to_agent with args: map[agent_name:prime_agent]
Bot calls tool: prime_checking with args: map[nums:[3]]
Bot: 3 is a prime number.
...
```

## Next Steps[¶](#next-steps "Permanent link")

Now that you have created an agent that's exposing a remote agent via an A2A server, the next step is to learn how to consume it from another agent.

* [**A2A Quickstart (Consuming)**](../quickstart-consuming-go/): Learn how your agent can use other agents using the A2A Protocol.

Back to top