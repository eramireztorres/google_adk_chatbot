---
url: https://google.github.io/adk-docs/observability/logging/
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
    - Logging

      [Logging](./)



      Table of contents
      * [Logging Philosophy](#logging-philosophy)
      * [How to Configure Logging](#how-to-configure-logging)

        + [Example Configuration](#example-configuration)
        + [Configuring Logging with the ADK CLI](#configuring-logging-with-the-adk-cli)
        + [Log Levels](#log-levels)
      * [Reading and Understanding the Logs](#reading-and-understanding-the-logs)
      * [Debugging with Logs: A Practical Example](#debugging-with-logs-a-practical-example)
    - [Cloud Trace](../cloud-trace/)
    - [AgentOps](../agentops/)
    - [Arize AX](../arize-ax/)
    - [Freeplay](../freeplay/)
    - [Monocle](../monocle/)
    - [Phoenix](../phoenix/)
    - [W&B Weave](../weave/)
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

* [Logging Philosophy](#logging-philosophy)
* [How to Configure Logging](#how-to-configure-logging)

  + [Example Configuration](#example-configuration)
  + [Configuring Logging with the ADK CLI](#configuring-logging-with-the-adk-cli)
  + [Log Levels](#log-levels)
* [Reading and Understanding the Logs](#reading-and-understanding-the-logs)
* [Debugging with Logs: A Practical Example](#debugging-with-logs-a-practical-example)

# Logging in the Agent Development Kit (ADK)[¶](#logging-in-the-agent-development-kit-adk "Permanent link")

Supported in ADKPython v0.1.0Go v0.1.0Java v0.1.0

The Agent Development Kit (ADK) uses Python's standard `logging` module to provide flexible and powerful logging capabilities. Understanding how to configure and interpret these logs is crucial for monitoring agent behavior and debugging issues effectively.

## Logging Philosophy[¶](#logging-philosophy "Permanent link")

ADK's approach to logging is to provide detailed diagnostic information without being overly verbose by default. It is designed to be configured by the application developer, allowing you to tailor the log output to your specific needs, whether in a development or production environment.

* **Standard Library:** It uses the standard `logging` library, so any configuration or handler that works with it will work with ADK.
* **Hierarchical Loggers:** Loggers are named hierarchically based on the module path (e.g., `google_adk.google.adk.agents.llm_agent`), allowing for fine-grained control over which parts of the framework produce logs.
* **User-Configured:** The framework does not configure logging itself. It is the responsibility of the developer using the framework to set up the desired logging configuration in their application's entry point.

## How to Configure Logging[¶](#how-to-configure-logging "Permanent link")

You can configure logging in your main application script (e.g., `main.py`) before you initialize and run your agent. The simplest way is to use `logging.basicConfig`.

### Example Configuration[¶](#example-configuration "Permanent link")

To enable detailed logging, including `DEBUG` level messages, add the following to the top of your script:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# Your ADK agent code follows...
# from google.adk.agents import LlmAgent
# ...
```

### Configuring Logging with the ADK CLI[¶](#configuring-logging-with-the-adk-cli "Permanent link")

When running agents using the ADK's built-in web or API servers, you can easily control the log verbosity directly from the command line. The `adk web`, `adk api_server`, and `adk deploy cloud_run` commands all accept a `--log_level` option.

This provides a convenient way to set the logging level without modifying your agent's source code.

> **Note:** The command-line setting always takes precedence over the programmatic configuration (like `logging.basicConfig`) for ADK's loggers. It's recommended to use `INFO` or `WARNING` in production and enable `DEBUG` only when troubleshooting.

**Example using `adk web`:**

To start the web server with `DEBUG` level logging, run:

```python
adk web --log_level DEBUG path/to/your/agents_dir
```

The available log levels for the `--log_level` option are:

* `DEBUG`
* `INFO` (default)
* `WARNING`
* `ERROR`
* `CRITICAL`

> You can also use `-v` or `--verbose` as a a shortcut for `--log_level DEBUG`.
>
> ```python
> adk web -v path/to/your/agents_dir
> ```

### Log Levels[¶](#log-levels "Permanent link")

ADK uses standard log levels to categorize messages. The configured level determines what information gets logged.

| Level | Description | Type of Information Logged |
| --- | --- | --- |
| **`DEBUG`** | **Crucial for debugging.** The most verbose level for fine-grained diagnostic information. | * **Full LLM Prompts:** The complete request sent to the language model, including system instructions, history, and tools. * Detailed API responses from services. * Internal state transitions and variable values. |
| **`INFO`** | General information about the agent's lifecycle. | * Agent initialization and startup. * Session creation and deletion events. * Execution of a tool, including its name and arguments. |
| **`WARNING`** | Indicates a potential issue or deprecated feature use. The agent continues to function, but attention may be required. | * Use of deprecated methods or parameters. * Non-critical errors that the system recovered from. |
| **`ERROR`** | A serious error that prevented an operation from completing. | * Failed API calls to external services (e.g., LLM, Session Service). * Unhandled exceptions during agent execution. * Configuration errors. |

> **Note:** It is recommended to use `INFO` or `WARNING` in production environments. Only enable `DEBUG` when actively troubleshooting an issue, as `DEBUG` logs can be very verbose and may contain sensitive information.

## Reading and Understanding the Logs[¶](#reading-and-understanding-the-logs "Permanent link")

The `format` string in the `basicConfig` example determines the structure of each log message.

Here’s a sample log entry:

```python
2025-07-08 11:22:33,456 - DEBUG - google_adk.google.adk.models.google_llm - LLM Request: contents { ... }
```

| Log Segment | Format Specifier | Meaning |
| --- | --- | --- |
| `2025-07-08 11:22:33,456` | `%(asctime)s` | Timestamp |
| `DEBUG` | `%(levelname)s` | Severity level |
| `google_adk.models.google_llm` | `%(name)s` | Logger name (the module that produced the log) |
| `LLM Request: contents { ... }` | `%(message)s` | The actual log message |

By reading the logger name, you can immediately pinpoint the source of the log and understand its context within the agent's architecture.

## Debugging with Logs: A Practical Example[¶](#debugging-with-logs-a-practical-example "Permanent link")

**Scenario:** Your agent is not producing the expected output, and you suspect the prompt being sent to the LLM is incorrect or missing information.

**Steps:**

1. **Enable DEBUG Logging:** In your `main.py`, set the logging level to `DEBUG` as shown in the configuration example.

   ```python
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
   )
   ```
2. **Run Your Agent:** Execute your agent's task as you normally would.
3. **Inspect the Logs:** Look through the console output for a message from the `google.adk.models.google_llm` logger that starts with `LLM Request:`.

   ```python
   ...
   2025-07-10 15:26:13,778 - DEBUG - google_adk.google.adk.models.google_llm - Sending out request, model: gemini-2.0-flash, backend: GoogleLLMVariant.GEMINI_API, stream: False
   2025-07-10 15:26:13,778 - DEBUG - google_adk.google.adk.models.google_llm - 
   LLM Request:
   -----------------------------------------------------------
   System Instruction:

         You roll dice and answer questions about the outcome of the dice rolls.
         You can roll dice of different sizes.
         You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
         It is ok to discuss previous dice roles, and comment on the dice rolls.
         When you are asked to roll a die, you must call the roll_die tool with the number of sides. Be sure to pass in an integer. Do not pass in a string.
         You should never roll a die on your own.
         When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
         You should not check prime numbers before calling the tool.
         When you are asked to roll a die and check prime numbers, you should always make the following two function calls:
         1. You should first call the roll_die tool to get a roll. Wait for the function response before calling the check_prime tool.
         2. After you get the function response from roll_die tool, you should call the check_prime tool with the roll_die result.
           2.1 If user asks you to check primes based on previous rolls, make sure you include the previous rolls in the list.
         3. When you respond, you must include the roll_die result from step 1.
         You should always perform the previous 3 steps when asking for a roll and checking prime numbers.
         You should not rely on the previous history on prime results.


   You are an agent. Your internal name is "hello_world_agent".

   The description about you is "hello world agent that can roll a dice of 8 sides and check prime numbers."
   -----------------------------------------------------------
   Contents:
   {"parts":[{"text":"Roll a 6 sided dice"}],"role":"user"}
   {"parts":[{"function_call":{"args":{"sides":6},"name":"roll_die"}}],"role":"model"}
   {"parts":[{"function_response":{"name":"roll_die","response":{"result":2}}}],"role":"user"}
   -----------------------------------------------------------
   Functions:
   roll_die: {'sides': {'type': <Type.INTEGER: 'INTEGER'>}} 
   check_prime: {'nums': {'items': {'type': <Type.INTEGER: 'INTEGER'>}, 'type': <Type.ARRAY: 'ARRAY'>}} 
   -----------------------------------------------------------

   2025-07-10 15:26:13,779 - INFO - google_genai.models - AFC is enabled with max remote calls: 10.
   2025-07-10 15:26:14,309 - INFO - google_adk.google.adk.models.google_llm - 
   LLM Response:
   -----------------------------------------------------------
   Text:
   I have rolled a 6 sided die, and the result is 2.
   ...
   ```
4. **Analyze the Prompt:** By examining the `System Instruction`, `contents`, `functions` sections of the logged request, you can verify:

   * Is the system instruction correct?
   * Is the conversation history (`user` and `model` turns) accurate?
   * Is the most recent user query included?
   * Are the correct tools being provided to the model?
   * Are the tools correctly called by the model?
   * How long it takes for the model to respond?

This detailed output allows you to diagnose a wide range of issues, from incorrect prompt engineering to problems with tool definitions, directly from the log files.

Back to top