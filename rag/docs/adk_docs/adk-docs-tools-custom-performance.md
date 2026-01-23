---
url: https://google.github.io/adk-docs/tools-custom/performance/
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
  + [Custom Tools](../)

    Custom Tools
    - Function tools




      Function tools
      * [Overview](../function-tools/)
      * Tool performance

        [Tool performance](./)



        Table of contents
        + [Build parallel-ready tools](#build-parallel-ready-tools)

          - [Example of http web call](#example-of-http-web-call)
          - [Example of database call](#example-of-database-call)
          - [Example of yielding behavior for long loops](#example-of-yielding-behavior-for-long-loops)
          - [Example of thread pools for intensive operations](#example-of-thread-pools-for-intensive-operations)
          - [Example of process chunking](#example-of-process-chunking)
        + [Write parallel-ready prompts and tool descriptions](#write-parallel-ready-prompts-and-tool-descriptions)
        + [Next steps](#next-steps)
      * [Action confirmations](../confirmation/)
    - [MCP tools](../mcp-tools/)
    - [OpenAPI tools](../openapi-tools/)
    - [Authentication](../authentication/)
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

* [Build parallel-ready tools](#build-parallel-ready-tools)

  + [Example of http web call](#example-of-http-web-call)
  + [Example of database call](#example-of-database-call)
  + [Example of yielding behavior for long loops](#example-of-yielding-behavior-for-long-loops)
  + [Example of thread pools for intensive operations](#example-of-thread-pools-for-intensive-operations)
  + [Example of process chunking](#example-of-process-chunking)
* [Write parallel-ready prompts and tool descriptions](#write-parallel-ready-prompts-and-tool-descriptions)
* [Next steps](#next-steps)

# Increase tool performance with parallel execution[¶](#increase-tool-performance-with-parallel-execution "Permanent link")

Supported in ADKPython v1.10.0

Starting with Agent Development Kit (ADK) version 1.10.0 for Python, the framework
attempts to run any agent-requested
[function tools](/adk-docs/tools-custom/function-tools/)
in parallel. This behavior can significantly improve the performance and
responsiveness of your agents, particularly for agents that rely on multiple
external APIs or long-running tasks. For example, if you have 3 tools that each
take 2 seconds, by running them in parallel, the total execution time will be
closer to 2 seconds, instead of 6 seconds. The ability to run tool functions
parallel can improve the performance of your agents, particularly in the
following scenarios:

* **Research tasks:** Where the agent collects information from multiple
  sources before proceeding to the next stage of the workflow.
* **API calls:** Where the agent accesses several APIs independently, such
  as searching for available flights using APIs from multiple airlines.
* **Publishing and communication tasks:** When the agent needs to publish
  or communicate through multiple, independent channels or multiple recipients.

However, your custom tools must be built with asynchronous execution support to
enable this performance improvement. This guide explains how parallel tool
execution works in the ADK and how to build your tools to take full advantage of
this processing feature.

Warning

Any ADK Tools that use synchronous processing in a set of tool function
calls will block other tools from executing in parallel, even if the other
tools allow for parallel execution.

## Build parallel-ready tools[¶](#build-parallel-ready-tools "Permanent link")

Enable parallel execution of your tool functions by defining them as
asynchronous functions. In Python code, this means using `async def` and `await`
syntax which allows the ADK to run them concurrently in an `asyncio` event loop.
The following sections show examples of agent tools built for parallel
processing and asynchronous operations.

### Example of http web call[¶](#example-of-http-web-call "Permanent link")

The following code example show how to modify the `get_weather()` function to
operate asynchronously and allow for parallel execution:

```python
 async def get_weather(city: str) -> dict:
      async with aiohttp.ClientSession() as session:
          async with session.get(f"http://api.weather.com/{city}") as response:
              return await response.json()
```

### Example of database call[¶](#example-of-database-call "Permanent link")

The following code example show how to write a database calling function to
operate asynchronously:

```python
async def query_database(query: str) -> list:
      async with asyncpg.connect("postgresql://...") as conn:
          return await conn.fetch(query)
```

### Example of yielding behavior for long loops[¶](#example-of-yielding-behavior-for-long-loops "Permanent link")

In cases where a tool is processing multiple requests or numerous long running
requests, consider adding yielding code to allow other tools to execute, as
shown in the following code sample:

```python
async def process_data(data: list) -> dict:
      results = []
      for i, item in enumerate(data):
          processed = await process_item(item)  # Yield point
          results.append(processed)

          # Add periodic yield points for long loops
          if i % 100 == 0:
              await asyncio.sleep(0)  # Yield control
      return {"results": results}
```

Important

Use the `asyncio.sleep()` function for pauses to avoid blocking
execution of other functions.

### Example of thread pools for intensive operations[¶](#example-of-thread-pools-for-intensive-operations "Permanent link")

When performing processing-intensive functions, consider creating thread pools
for better management of available computing resources, as shown in the
following example:

```python
async def cpu_intensive_tool(data: list) -> dict:
      loop = asyncio.get_event_loop()

      # Use thread pool for CPU-bound work
      with ThreadPoolExecutor() as executor:
          result = await loop.run_in_executor(
              executor,
              expensive_computation,
              data
          )
      return {"result": result}
```

### Example of process chunking[¶](#example-of-process-chunking "Permanent link")

When performing processes on long lists or large amounts of data, consider
combining a thread pool technique with dividing up processing into chunks of
data, and yielding processing time between the chunks, as shown in the following
example:

```python
 async def process_large_dataset(dataset: list) -> dict:
      results = []
      chunk_size = 1000

      for i in range(0, len(dataset), chunk_size):
          chunk = dataset[i:i + chunk_size]

          # Process chunk in thread pool
          loop = asyncio.get_event_loop()
          with ThreadPoolExecutor() as executor:
              chunk_result = await loop.run_in_executor(
                  executor, process_chunk, chunk
              )

          results.extend(chunk_result)

          # Yield control between chunks
          await asyncio.sleep(0)

      return {"total_processed": len(results), "results": results}
```

## Write parallel-ready prompts and tool descriptions[¶](#write-parallel-ready-prompts-and-tool-descriptions "Permanent link")

When building prompts for AI models, consider explicitly specifying or hinting
that function calls be made in parallel. The following example of an AI prompt
directs the model to use tools in parallel:

```python
When users ask for multiple pieces of information, always call functions in
parallel.

  Examples:
  - "Get weather for London and currency rate USD to EUR" → Call both functions
    simultaneously
  - "Compare cities A and B" → Call get_weather, get_population, get_distance in 
    parallel
  - "Analyze multiple stocks" → Call get_stock_price for each stock in parallel

  Always prefer multiple specific function calls over single complex calls.
```

The following example shows a tool function description that hints at more
efficient use through parallel execution:

```python
 async def get_weather(city: str) -> dict:
      """Get current weather for a single city.

      This function is optimized for parallel execution - call multiple times for different cities.

      Args:
          city: Name of the city, for example: 'London', 'New York'

      Returns:
          Weather data including temperature, conditions, humidity
      """
      await asyncio.sleep(2)  # Simulate API call
      return {"city": city, "temp": 72, "condition": "sunny"}
```

## Next steps[¶](#next-steps "Permanent link")

For more information on building Tools for agents and function calling, see
[Function Tools](/adk-docs/tools-custom/function-tools/). For
more detailed examples of tools that take advantage of parallel processing, see
the samples in the
[adk-python](https://github.com/google/adk-python/tree/main/contributing/samples/parallel_functions)
repository.

Back to top