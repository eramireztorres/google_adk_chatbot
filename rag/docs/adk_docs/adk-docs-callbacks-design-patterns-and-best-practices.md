---
url: https://google.github.io/adk-docs/callbacks/design-patterns-and-best-practices/
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
  + [Callbacks](../)

    Callbacks
    - [Types of callbacks](../types-of-callbacks/)
    - Callback patterns

      [Callback patterns](./)



      Table of contents
      * [Design Patterns](#design-patterns)

        + [1. Guardrails & Policy Enforcement](#guardrails-policy-enforcement)
        + [2. Dynamic State Management](#dynamic-state-management)
        + [3. Logging and Monitoring](#logging-and-monitoring)
        + [4. Caching](#caching)
        + [5. Request/Response Modification](#request-response-modification)
        + [6. Conditional Skipping of Steps](#conditional-skipping-of-steps)
        + [7. Tool-Specific Actions (Authentication & Summarization Control)](#tool-specific-actions-authentication-summarization-control)
        + [8. Artifact Handling](#artifact-handling)
      * [Best Practices for Callbacks](#best-practices-for-callbacks)

        + [Design Principles](#design-principles)
        + [Error Handling](#error-handling)
        + [State Management](#state-management)
        + [Reliability](#reliability)
        + [Testing & Documentation](#testing-documentation)
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

* [Design Patterns](#design-patterns)

  + [1. Guardrails & Policy Enforcement](#guardrails-policy-enforcement)
  + [2. Dynamic State Management](#dynamic-state-management)
  + [3. Logging and Monitoring](#logging-and-monitoring)
  + [4. Caching](#caching)
  + [5. Request/Response Modification](#request-response-modification)
  + [6. Conditional Skipping of Steps](#conditional-skipping-of-steps)
  + [7. Tool-Specific Actions (Authentication & Summarization Control)](#tool-specific-actions-authentication-summarization-control)
  + [8. Artifact Handling](#artifact-handling)
* [Best Practices for Callbacks](#best-practices-for-callbacks)

  + [Design Principles](#design-principles)
  + [Error Handling](#error-handling)
  + [State Management](#state-management)
  + [Reliability](#reliability)
  + [Testing & Documentation](#testing-documentation)

# Design Patterns and Best Practices for Callbacks[¶](#design-patterns-and-best-practices-for-callbacks "Permanent link")

Callbacks offer powerful hooks into the agent lifecycle. Here are common design patterns illustrating how to leverage them effectively in ADK, followed by best practices for implementation.

## Design Patterns[¶](#design-patterns "Permanent link")

These patterns demonstrate typical ways to enhance or control agent behavior using callbacks:

### 1. Guardrails & Policy Enforcement[¶](#guardrails-policy-enforcement "Permanent link")

**Pattern Overview:**
Intercept requests before they reach the LLM or tools to enforce rules.

**Implementation:**
- Use `before_model_callback` to inspect the `LlmRequest` prompt
- Use `before_tool_callback` to inspect tool arguments
- If a policy violation is detected (e.g., forbidden topics, profanity):
- Return a predefined response (`LlmResponse` or `dict`/`Map`) to block the operation
- Optionally update `context.state` to log the violation

**Example Use Case:**
A `before_model_callback` checks `llm_request.contents` for sensitive keywords and returns a standard "Cannot process this request" `LlmResponse` if found, preventing the LLM call.

### 2. Dynamic State Management[¶](#dynamic-state-management "Permanent link")

**Pattern Overview:**
Read from and write to session state within callbacks to make agent behavior context-aware and pass data between steps.

**Implementation:**
- Access `callback_context.state` or `tool_context.state`
- Modifications (`state['key'] = value`) are automatically tracked in the subsequent `Event.actions.state_delta`
- Changes are persisted by the `SessionService`

**Example Use Case:**
An `after_tool_callback` saves a `transaction_id` from the tool's result to `tool_context.state['last_transaction_id']`. A later `before_agent_callback` might read `state['user_tier']` to customize the agent's greeting.

### 3. Logging and Monitoring[¶](#logging-and-monitoring "Permanent link")

**Pattern Overview:**
Add detailed logging at specific lifecycle points for observability and debugging.

**Implementation:**
- Implement callbacks (e.g., `before_agent_callback`, `after_tool_callback`, `after_model_callback`)
- Print or send structured logs containing:
- Agent name
- Tool name
- Invocation ID
- Relevant data from the context or arguments

**Example Use Case:**
Log messages like `INFO: [Invocation: e-123] Before Tool: search_api - Args: {'query': 'ADK'}`.

### 4. Caching[¶](#caching "Permanent link")

**Pattern Overview:**
Avoid redundant LLM calls or tool executions by caching results.

**Implementation Steps:**
1. **Before Operation:** In `before_model_callback` or `before_tool_callback`:
- Generate a cache key based on the request/arguments
- Check `context.state` (or an external cache) for this key
- If found, return the cached `LlmResponse` or result directly

1. **After Operation:** If cache miss occurred:
2. Use the corresponding `after_` callback to store the new result in the cache using the key

**Example Use Case:**
`before_tool_callback` for `get_stock_price(symbol)` checks `state[f"cache:stock:{symbol}"]`. If present, returns the cached price; otherwise, allows the API call and `after_tool_callback` saves the result to the state key.

### 5. Request/Response Modification[¶](#request-response-modification "Permanent link")

**Pattern Overview:**
Alter data just before it's sent to the LLM/tool or just after it's received.

**Implementation Options:**
- **`before_model_callback`:** Modify `llm_request` (e.g., add system instructions based on `state`)
- **`after_model_callback`:** Modify the returned `LlmResponse` (e.g., format text, filter content)
- **`before_tool_callback`:** Modify the tool `args` dictionary (or Map in Java)
- **`after_tool_callback`:** Modify the `tool_response` dictionary (or Map in Java)

**Example Use Case:**
`before_model_callback` appends "User language preference: Spanish" to `llm_request.config.system_instruction` if `context.state['lang'] == 'es'`.

### 6. Conditional Skipping of Steps[¶](#conditional-skipping-of-steps "Permanent link")

**Pattern Overview:**
Prevent standard operations (agent run, LLM call, tool execution) based on certain conditions.

**Implementation:**
- Return a value from a `before_` callback to skip the normal execution:
- `Content` from `before_agent_callback`
- `LlmResponse` from `before_model_callback`
- `dict` from `before_tool_callback`
- The framework interprets this returned value as the result for that step

**Example Use Case:**
`before_tool_callback` checks `tool_context.state['api_quota_exceeded']`. If `True`, it returns `{'error': 'API quota exceeded'}`, preventing the actual tool function from running.

### 7. Tool-Specific Actions (Authentication & Summarization Control)[¶](#tool-specific-actions-authentication-summarization-control "Permanent link")

**Pattern Overview:**
Handle actions specific to the tool lifecycle, primarily authentication and controlling LLM summarization of tool results.

**Implementation:**
Use `ToolContext` within tool callbacks (`before_tool_callback`, `after_tool_callback`):

* **Authentication:** Call `tool_context.request_credential(auth_config)` in `before_tool_callback` if credentials are required but not found (e.g., via `tool_context.get_auth_response` or state check). This initiates the auth flow.
* **Summarization:** Set `tool_context.actions.skip_summarization = True` if the raw dictionary output of the tool should be passed back to the LLM or potentially displayed directly, bypassing the default LLM summarization step.

**Example Use Case:**
A `before_tool_callback` for a secure API checks for an auth token in state; if missing, it calls `request_credential`. An `after_tool_callback` for a tool returning structured JSON might set `skip_summarization = True`.

### 8. Artifact Handling[¶](#artifact-handling "Permanent link")

**Pattern Overview:**
Save or load session-related files or large data blobs during the agent lifecycle.

**Implementation:**
- **Saving:** Use `callback_context.save_artifact` / `await tool_context.save_artifact` to store data:
- Generated reports
- Logs
- Intermediate data
- **Loading:** Use `load_artifact` to retrieve previously stored artifacts
- **Tracking:** Changes are tracked via `Event.actions.artifact_delta`

**Example Use Case:**
An `after_tool_callback` for a "generate\_report" tool saves the output file using `await tool_context.save_artifact("report.pdf", report_part)`. A `before_agent_callback` might load a configuration artifact using `callback_context.load_artifact("agent_config.json")`.

## Best Practices for Callbacks[¶](#best-practices-for-callbacks "Permanent link")

### Design Principles[¶](#design-principles "Permanent link")

**Keep Focused:**
Design each callback for a single, well-defined purpose (e.g., just logging, just validation). Avoid monolithic callbacks.

**Mind Performance:**
Callbacks execute synchronously within the agent's processing loop. Avoid long-running or blocking operations (network calls, heavy computation). Offload if necessary, but be aware this adds complexity.

### Error Handling[¶](#error-handling "Permanent link")

**Handle Errors Gracefully:**
- Use `try...except/catch` blocks within your callback functions
- Log errors appropriately
- Decide if the agent invocation should halt or attempt recovery
- Don't let callback errors crash the entire process

### State Management[¶](#state-management "Permanent link")

**Manage State Carefully:**
- Be deliberate about reading from and writing to `context.state`
- Changes are immediately visible within the *current* invocation and persisted at the end of the event processing
- Use specific state keys rather than modifying broad structures to avoid unintended side effects
- Consider using state prefixes (`State.APP_PREFIX`, `State.USER_PREFIX`, `State.TEMP_PREFIX`) for clarity, especially with persistent `SessionService` implementations

### Reliability[¶](#reliability "Permanent link")

**Consider Idempotency:**
If a callback performs actions with external side effects (e.g., incrementing an external counter), design it to be idempotent (safe to run multiple times with the same input) if possible, to handle potential retries in the framework or your application.

### Testing & Documentation[¶](#testing-documentation "Permanent link")

**Test Thoroughly:**
- Unit test your callback functions using mock context objects
- Perform integration tests to ensure callbacks function correctly within the full agent flow

**Ensure Clarity:**
- Use descriptive names for your callback functions
- Add clear docstrings explaining their purpose, when they run, and any side effects (especially state modifications)

**Use Correct Context Type:**
Always use the specific context type provided (`CallbackContext` for agent/model, `ToolContext` for tools) to ensure access to the appropriate methods and properties.

By applying these patterns and best practices, you can effectively use callbacks to create more robust, observable, and customized agent behaviors in ADK.

Back to top