---
url: https://google.github.io/adk-docs/a2a/quickstart-consuming/
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
      * Python

        [Python](./)



        Table of contents
        + [Overview](#overview)
        + [Exposing Your Agent with the ADK Server](#exposing-your-agent-with-the-adk-server)

          - [1. Getting the Sample Code](#getting-the-sample-code)

            * [Main Agent (a2a\_basic/agent.py)](#main-agent-a2a_basicagentpy)
            * [Remote Prime Agent (a2a\_basic/remote\_a2a/check\_prime\_agent/)](#remote-prime-agent-a2a_basicremote_a2acheck_prime_agent)
          - [2. Start the Remote Prime Agent server](#start-the-remote-prime-agent-server)
          - [3. Look out for the required agent card (agent-card.json) of the remote agent](#look-out-for-the-required-agent-card-agent-json-of-the-remote-agent)
          - [4. Run the Main (Consuming) Agent](#run-the-main-consuming-agent)

            * [How it works](#how-it-works)
        + [Example Interactions](#example-interactions)
        + [Next Steps](#next-steps)
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
* [Exposing Your Agent with the ADK Server](#exposing-your-agent-with-the-adk-server)

  + [1. Getting the Sample Code](#getting-the-sample-code)

    - [Main Agent (a2a\_basic/agent.py)](#main-agent-a2a_basicagentpy)
    - [Remote Prime Agent (a2a\_basic/remote\_a2a/check\_prime\_agent/)](#remote-prime-agent-a2a_basicremote_a2acheck_prime_agent)
  + [2. Start the Remote Prime Agent server](#start-the-remote-prime-agent-server)
  + [3. Look out for the required agent card (agent-card.json) of the remote agent](#look-out-for-the-required-agent-card-agent-json-of-the-remote-agent)
  + [4. Run the Main (Consuming) Agent](#run-the-main-consuming-agent)

    - [How it works](#how-it-works)
* [Example Interactions](#example-interactions)
* [Next Steps](#next-steps)

# Quickstart: Consuming a remote agent via A2A[¶](#quickstart-consuming-a-remote-agent-via-a2a "Permanent link")

Supported in ADKPythonExperimental

This quickstart covers the most common starting point for any developer: **"There is a remote agent, how do I let my ADK agent use it via A2A?"**. This is crucial for building complex multi-agent systems where different agents need to collaborate and interact.

## Overview[¶](#overview "Permanent link")

This sample demonstrates the **Agent2Agent (A2A)** architecture in the Agent Development Kit (ADK), showcasing how multiple agents can work together to handle complex tasks. The sample implements an agent that can roll dice and check if numbers are prime.

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

The ADK comes with a built-in CLI command, `adk api_server --a2a` to expose your agent using the A2A protocol.

In the `a2a_basic` example, you will first need to expose the `check_prime_agent` via an A2A server, so that the local root agent can use it.

### 1. Getting the Sample Code[¶](#getting-the-sample-code "Permanent link")

First, make sure you have the necessary dependencies installed:

```python
pip install google-adk[a2a]
```

You can clone and navigate to the [**`a2a_basic`** sample](https://github.com/google/adk-python/tree/main/contributing/samples/a2a_basic) here:

```python
git clone https://github.com/google/adk-python.git
```

As you'll see, the folder structure is as follows:

```python
a2a_basic/
├── remote_a2a/
│   └── check_prime_agent/
│       ├── __init__.py
│       ├── agent.json
│       └── agent.py
├── README.md
├── __init__.py
└── agent.py # local root agent
```

#### Main Agent (`a2a_basic/agent.py`)[¶](#main-agent-a2a_basicagentpy "Permanent link")

* **`roll_die(sides: int)`**: Function tool for rolling dice
* **`roll_agent`**: Local agent specialized in dice rolling
* **`prime_agent`**: Remote A2A agent configuration
* **`root_agent`**: Main orchestrator with delegation logic

#### Remote Prime Agent (`a2a_basic/remote_a2a/check_prime_agent/`)[¶](#remote-prime-agent-a2a_basicremote_a2acheck_prime_agent "Permanent link")

* **`agent.py`**: Implementation of the prime checking service
* **`agent.json`**: Agent card of the A2A agent
* **`check_prime(nums: list[int])`**: Prime number checking algorithm

### 2. Start the Remote Prime Agent server[¶](#start-the-remote-prime-agent-server "Permanent link")

To show how your ADK agent can consume a remote agent via A2A, you'll first need to start a remote agent server, which will host the prime agent (under `check_prime_agent`).

```python
# Start the remote a2a server that serves the check_prime_agent on port 8001
adk api_server --a2a --port 8001 contributing/samples/a2a_basic/remote_a2a
```

Adding logging for debugging with `--log_level debug`

To enable debug-level logging, you can add `--log_level debug` to your `adk api_server`, as in:

```python
adk api_server --a2a --port 8001 contributing/samples/a2a_basic/remote_a2a --log_level debug
```

This will give richer logs for you to inspect when testing your agents.


Why use port 8001?

In this quickstart, when testing locally, your agents will be using localhost, so the `port` for the A2A server for the exposed agent (the remote, prime agent) must be different from the consuming agent's port. The default port for `adk web` where you will interact with the consuming agent is `8000`, which is why the A2A server is created using a separate port, `8001`.

Once executed, you should see something like:

```python
INFO:     Started server process [56558]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
```

### 3. Look out for the required agent card (`agent-card.json`) of the remote agent[¶](#look-out-for-the-required-agent-card-agent-json-of-the-remote-agent "Permanent link")

A2A Protocol requires that each agent must have an agent card that describes what it does.

If someone else has already built the remote A2A agent that you are looking to consume in your agent, then you should confirm that they have an agent card (`agent-card.json`).

In the sample, the `check_prime_agent` already has an agent card provided:

a2a\_basic/remote\_a2a/check\_prime\_agent/agent-card.json

```python
{
  "capabilities": {},
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["application/json"],
  "description": "An agent specialized in checking whether numbers are prime. It can efficiently determine the primality of individual numbers or lists of numbers.",
  "name": "check_prime_agent",
  "skills": [
    {
      "id": "prime_checking",
      "name": "Prime Number Checking",
      "description": "Check if numbers in a list are prime using efficient mathematical algorithms",
      "tags": ["mathematical", "computation", "prime", "numbers"]
    }
  ],
  "url": "http://localhost:8001/a2a/check_prime_agent",
  "version": "1.0.0"
}
```

More info on agent cards in ADK

In ADK, you can use a `to_a2a(root_agent)` wrapper which automatically generates an agent card for you. If you're interested in learning more about how to expose your existing agent so others can use it, then please look at the [A2A Quickstart (Exposing)](../quickstart-exposing/) tutorial.

### 4. Run the Main (Consuming) Agent[¶](#run-the-main-consuming-agent "Permanent link")

```python
# In a separate terminal, run the adk web server
adk web contributing/samples/
```

#### How it works[¶](#how-it-works "Permanent link")

The main agent uses the `RemoteA2aAgent()` function to consume the remote agent (`prime_agent` in our example). As you can see below, `RemoteA2aAgent()` requires the `name`, `description`, and the URL of the `agent_card`.

a2a\_basic/agent.py

```python
<...code truncated...>

from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

prime_agent = RemoteA2aAgent(
    name="prime_agent",
    description="Agent that handles checking if numbers are prime.",
    agent_card=(
        f"http://localhost:8001/a2a/check_prime_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

<...code truncated>
```

Then, you can simply use the `RemoteA2aAgent` in your agent. In this case, `prime_agent` is used as one of the sub-agents in the `root_agent` below:

a2a\_basic/agent.py

```python
from google.adk.agents.llm_agent import Agent
from google.genai import types

root_agent = Agent(
    model="gemini-2.0-flash",
    name="root_agent",
    instruction="""
      <You are a helpful assistant that can roll dice and check if numbers are prime.
      You delegate rolling dice tasks to the roll_agent and prime checking tasks to the prime_agent.
      Follow these steps:
      1. If the user asks to roll a die, delegate to the roll_agent.
      2. If the user asks to check primes, delegate to the prime_agent.
      3. If the user asks to roll a die and then check if the result is prime, call roll_agent first, then pass the result to prime_agent.
      Always clarify the results before proceeding.>
    """,
    global_instruction=(
        "You are DicePrimeBot, ready to roll dice and check prime numbers."
    ),
    sub_agents=[roll_agent, prime_agent],
    tools=[example_tool],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(  # avoid false alarm about rolling dice.
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
```

## Example Interactions[¶](#example-interactions "Permanent link")

Once both your main and remote agents are running, you can interact with the root agent to see how it calls the remote agent via A2A:

**Simple Dice Rolling:**
This interaction uses a local agent, the Roll Agent:

```python
User: Roll a 6-sided die
Bot: I rolled a 4 for you.
```

**Prime Number Checking:**

This interaction uses a remote agent via A2A, the Prime Agent:

```python
User: Is 7 a prime number?
Bot: Yes, 7 is a prime number.
```

**Combined Operations:**

This interaction uses both the local Roll Agent and the remote Prime Agent:

```python
User: Roll a 10-sided die and check if it's prime
Bot: I rolled an 8 for you.
Bot: 8 is not a prime number.
```

## Next Steps[¶](#next-steps "Permanent link")

Now that you have created an agent that's using a remote agent via an A2A server, the next step is to learn how to connect to it from another agent.

* [**A2A Quickstart (Exposing)**](../quickstart-exposing/): Learn how to expose your existing agent so that other agents can use it via the A2A Protocol.

Back to top