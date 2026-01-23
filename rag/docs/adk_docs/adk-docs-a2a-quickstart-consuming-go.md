---
url: https://google.github.io/adk-docs/a2a/quickstart-consuming-go/
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
      * [Go](../quickstart-exposing-go/)
    - A2A Quickstart (Consuming)




      A2A Quickstart (Consuming)
      * [Python](../quickstart-consuming/)
      * Go

        [Go](./)



        Table of contents
        + [Overview](#overview)
        + [Exposing Your Agent with the ADK Server](#exposing-your-agent-with-the-adk-server)

          - [1. Getting the Sample Code](#getting-the-sample-code)

            * [Main Agent (a2a\_basic/main.go)](#main-agent-a2a_basicmaingo)
            * [Remote Prime Agent (a2a\_basic/remote\_a2a/check\_prime\_agent/main.go)](#remote-prime-agent-a2a_basicremote_a2acheck_prime_agentmaingo)
          - [2. Start the Remote Prime Agent server](#start-the-remote-prime-agent-server)
          - [3. Look out for the required agent card of the remote agent](#look-out-for-the-required-agent-card-of-the-remote-agent)
          - [4. Run the Main (Consuming) Agent](#run-the-main-consuming-agent)

            * [How it works](#how-it-works)
        + [Example Interactions](#example-interactions)
        + [Next Steps](#next-steps)
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
* [Exposing Your Agent with the ADK Server](#exposing-your-agent-with-the-adk-server)

  + [1. Getting the Sample Code](#getting-the-sample-code)

    - [Main Agent (a2a\_basic/main.go)](#main-agent-a2a_basicmaingo)
    - [Remote Prime Agent (a2a\_basic/remote\_a2a/check\_prime\_agent/main.go)](#remote-prime-agent-a2a_basicremote_a2acheck_prime_agentmaingo)
  + [2. Start the Remote Prime Agent server](#start-the-remote-prime-agent-server)
  + [3. Look out for the required agent card of the remote agent](#look-out-for-the-required-agent-card-of-the-remote-agent)
  + [4. Run the Main (Consuming) Agent](#run-the-main-consuming-agent)

    - [How it works](#how-it-works)
* [Example Interactions](#example-interactions)
* [Next Steps](#next-steps)

# Quickstart: Consuming a remote agent via A2A[¶](#quickstart-consuming-a-remote-agent-via-a2a "Permanent link")

Supported in ADKGoExperimental

This quickstart covers the most common starting point for any developer: **"There is a remote agent, how do I let my ADK agent use it via A2A?"**. This is crucial for building complex multi-agent systems where different agents need to collaborate and interact.

## Overview[¶](#overview "Permanent link")

This sample demonstrates the **Agent-to-Agent (A2A)** architecture in the Agent Development Kit (ADK), showcasing how multiple agents can work together to handle complex tasks. The sample implements an agent that can roll dice and check if numbers are prime.

```python
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│   Root Agent    │───▶│   Roll Agent     │    │   Remote Prime     │
│  (Local)        │    │   (Local)        │    │   Agent            │
│                 │    │                  │    │  (localhost:8001)  │
│                 │───▶│                  │◀───│                    │
└─────────────────┘    └──────────────────┘    └────────────────────┘
```

The A2A Basic sample consists of:

* **Root Agent** (`root_agent`): The main orchestrator that delegates tasks to specialized sub-agents
* **Roll Agent** (`roll_agent`): A local sub-agent that handles dice rolling operations
* **Prime Agent** (`prime_agent`): A remote A2A agent that checks if numbers are prime, this agent is running on a separate A2A server

## Exposing Your Agent with the ADK Server[¶](#exposing-your-agent-with-the-adk-server "Permanent link")

In the `a2a_basic` example, you will first need to expose the `check_prime_agent` via an A2A server, so that the local root agent can use it.

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
│       └── main.go
├── go.mod
├── go.sum
└── main.go # local root agent
```

#### Main Agent (`a2a_basic/main.go`)[¶](#main-agent-a2a_basicmaingo "Permanent link")

* **`rollDieTool`**: Function tool for rolling dice
* **`newRollAgent`**: Local agent specialized in dice rolling
* **`newPrimeAgent`**: Remote A2A agent configuration
* **`newRootAgent`**: Main orchestrator with delegation logic

#### Remote Prime Agent (`a2a_basic/remote_a2a/check_prime_agent/main.go`)[¶](#remote-prime-agent-a2a_basicremote_a2acheck_prime_agentmaingo "Permanent link")

* **`checkPrimeTool`**: Prime number checking algorithm
* **`main`**: Implementation of the prime checking service and A2A server.

### 2. Start the Remote Prime Agent server[¶](#start-the-remote-prime-agent-server "Permanent link")

To show how your ADK agent can consume a remote agent via A2A, you'll first need to start a remote agent server, which will host the prime agent (under `check_prime_agent`).

```python
# Start the remote a2a server that serves the check_prime_agent on port 8001
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

### 3. Look out for the required agent card of the remote agent[¶](#look-out-for-the-required-agent-card-of-the-remote-agent "Permanent link")

A2A Protocol requires that each agent must have an agent card that describes what it does.

In the Go ADK, the agent card is generated dynamically when you expose an agent using the A2A launcher. You can visit `http://localhost:8001/.well-known/agent-card.json` to see the generated card.

### 4. Run the Main (Consuming) Agent[¶](#run-the-main-consuming-agent "Permanent link")

```python
# In a separate terminal, run the main agent
go run main.go
```

#### How it works[¶](#how-it-works "Permanent link")

The main agent uses `remoteagent.New` to consume the remote agent (`prime_agent` in our example). As you can see below, it requires the `Name`, `Description`, and the `AgentCardSource` URL.

a2a\_basic/main.go

```python
func newPrimeAgent() (agent.Agent, error) {
    remoteAgent, err := remoteagent.New(remoteagent.A2AConfig{
        Name:            "prime_agent",
        Description:     "Agent that handles checking if numbers are prime.",
        AgentCardSource: "http://localhost:8001",
    })
    if err != nil {
        return nil, fmt.Errorf("failed to create remote prime agent: %w", err)
    }
    return remoteAgent, nil
}
```

Then, you can simply use the remote agent in your root agent. In this case, `primeAgent` is used as one of the sub-agents in the `root_agent` below:

a2a\_basic/main.go

```python
func newRootAgent(ctx context.Context, rollAgent, primeAgent agent.Agent) (agent.Agent, error) {
    model, err := gemini.NewModel(ctx, "gemini-2.0-flash", &genai.ClientConfig{})
    if err != nil {
        return nil, err
    }
    return llmagent.New(llmagent.Config{
        Name:  "root_agent",
        Model: model,
        Instruction: `
      You are a helpful assistant that can roll dice and check if numbers are prime.
      You delegate rolling dice tasks to the roll_agent and prime checking tasks to the prime_agent.
      Follow these steps:
      1. If the user asks to roll a die, delegate to the roll_agent.
      2. If the user asks to check primes, delegate to the prime_agent.
      3. If the user asks to roll a die and then check if the result is prime, call roll_agent first, then pass the result to prime_agent.
      Always clarify the results before proceeding.
    `,
        SubAgents: []agent.Agent{rollAgent, primeAgent},
        Tools:     []tool.Tool{},
    })
}
```

## Example Interactions[¶](#example-interactions "Permanent link")

Once both your main and remote agents are running, you can interact with the root agent to see how it calls the remote agent via A2A:

**Simple Dice Rolling:**
This interaction uses a local agent, the Roll Agent:

```python
User: Roll a 6-sided die
Bot calls tool: transfer_to_agent with args: map[agent_name:roll_agent]
Bot calls tool: roll_die with args: map[sides:6]
Bot: I rolled a 6-sided die and the result is 6.
```

**Prime Number Checking:**

This interaction uses a remote agent via A2A, the Prime Agent:

```python
User: Is 7 a prime number?
Bot calls tool: transfer_to_agent with args: map[agent_name:prime_agent]
Bot calls tool: prime_checking with args: map[nums:[7]]
Bot: Yes, 7 is a prime number.
```

**Combined Operations:**

This interaction uses both the local Roll Agent and the remote Prime Agent:

```python
User: roll a die and check if it's a prime
Bot: Okay, I will first roll a die and then check if the result is a prime number.

Bot calls tool: transfer_to_agent with args: map[agent_name:roll_agent]
Bot calls tool: roll_die with args: map[sides:6]
Bot calls tool: transfer_to_agent with args: map[agent_name:prime_agent]
Bot calls tool: prime_checking with args: map[nums:[3]]
Bot: 3 is a prime number.
```

## Next Steps[¶](#next-steps "Permanent link")

Now that you have created an agent that's using a remote agent via an A2A server, the next step is to learn how to expose your own agent.

* [**A2A Quickstart (Exposing)**](../quickstart-exposing-go/): Learn how to expose your existing agent so that other agents can use it via the A2A Protocol.

Back to top