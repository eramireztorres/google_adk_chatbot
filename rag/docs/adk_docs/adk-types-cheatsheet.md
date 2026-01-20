# Google ADK Types and Classes Cheat Sheet

This is a quick reference to the main ADK types/classes and when you use them.
It is based on the docs in `docs/adk_docs`.

## Core Agent Types

- `Agent` (alias of `LlmAgent`): Default LLM-powered agent type.
- `BaseAgent`: Root class for all agents; defines the `run_async` contract and agent hierarchy.
- `LlmAgent`: Uses an LLM to decide actions; configured via `instruction`, `tools`, `model`, schemas, and optional `planner`/`code_executor`.

## Workflow Agents (Deterministic Orchestration)

- `SequentialAgent`: Runs sub-agents in strict order; shares one `InvocationContext` across steps.
- `LoopAgent`: Repeats sub-agents until a termination signal or `max_iterations`.
- `ParallelAgent`: Runs sub-agents concurrently in separate branches; no automatic shared state.

## Custom Agents (Full Control)

- Custom agent = subclass of `BaseAgent` implementing `_run_async_impl` (or `runAsyncImpl`).
- Used when predefined workflow agents are not enough; you orchestrate sub-agents and yield `Event`s directly.

## Planning and Code Execution

- `BasePlanner`: Interface for planners that structure multi-step reasoning.
- `BuiltInPlanner`: Built-in planning strategy for multi-step tool use.
- `PlanReActPlanner`: Enforces a plan-then-act structure (useful for models without built-in reasoning).
- `BaseCodeExecutor`: Interface for executing code blocks in model output.
- `BuiltInCodeExecutor`: Executes code via the built-in execution flow.
- `UnsafeLocalCodeExecutor`: Local code execution (use with care).
- `CodeExecutorContext`: Tracks execution state, errors, and file inputs for code execution.

## Tool Types and Toolsets

- Core abstractions (use to define and compose tools)
  - `BaseTool`: Base class for all tools.
  - `FunctionTool`: Wraps a Python/Go/Java function as a tool.
  - `LongRunningFunctionTool`: Tool that signals long-running behavior; affects `Event` final-response handling.
  - `AgentTool`: Wraps an agent so another agent can call it as a tool.
  - `BaseToolset`: Base class for grouped tools with shared lifecycle/config.
- Auth and confirmation (use when tools require credentials/consent)
  - `BaseAuthenticatedTool`, `AuthenticatedFunctionTool`: Tools that require auth and use tool auth flow.
  - `AuthToolArguments`: Payload used when requesting auth within tools.
- MCP tools (use to expose MCP servers to agents)
  - `MCPToolset`/`McpToolset`: Loads tools from an MCP server.
  - `MCPTool`/`McpTool`: Single MCP-backed tool wrapper.
- OpenAPI tools (use to auto-generate tools from REST specs)
  - `OpenAPIToolset`: Generates callable tools from an OpenAPI spec.
  - `RestApiTool`: Represents a single OpenAPI operation.
- Grounding and search tools (use for web or enterprise search grounding)
  - `GoogleSearchTool`: Google Search grounding tool.
  - `VertexAiSearchTool`: Vertex AI Search grounding tool.
  - `DiscoveryEngineSearchTool`: Discovery Engine search tool.
- Google API toolsets (use to access Google Workspace/YouTube APIs)
  - `GoogleApiToolset`: Base for Google API tool families.
  - `GmailToolset`, `DocsToolset`, `SheetsToolset`, `SlidesToolset`, `CalendarToolset`, `YoutubeToolset`.
  - `GoogleApiTool`: Single Google API tool wrapper with auth helpers.
- Google Cloud database toolsets (use for DB access and analytics)
  - `BigQueryToolset`: BigQuery tools.
  - `BigtableToolset`: Bigtable tools.
  - `SpannerToolset`: Spanner tools.
  - `ToolboxToolset`: MCP Toolbox for Databases integration.
- Memory and artifacts tools (use for long-term memory and file artifacts)
  - `LoadMemoryTool`: Search memory from inside a tool call.
  - `PreloadMemoryTool`: Preloads memory for a session/agent.
  - `LoadArtifactsTool`: Loads artifacts by name/version.
  - `UrlContextTool`: Fetches URL content into context.
  - `BaseRetrievalTool`: Base for retrieval-style tools.

### Tool Group Examples (Python, Minimal)

```python
# Core abstractions: wrap a function as a tool.
from google.adk.tools import FunctionTool, ToolContext

def get_time(tool_context: ToolContext) -> dict:
    return {"time": "12:00"}

time_tool = FunctionTool(func=get_time, name="get_time")
```

```python
# Auth and confirmation: require credentials for a tool.
from google.adk.tools import AuthenticatedFunctionTool

secure_tool = AuthenticatedFunctionTool(func=secure_call, auth_config=MY_AUTH_CONFIG)
```

```python
# MCP tools: load tools from an MCP server.
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

mcp_toolset = MCPToolset(connection_params=mcp_connection)
```

```python
# OpenAPI tools: create tools from an OpenAPI spec.
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

toolset = OpenAPIToolset(spec_str=openapi_spec_json, spec_str_type="json")
```

```python
# Grounding/search tools: use built-in search grounding.
from google.adk.tools import GoogleSearchTool

search_tool = GoogleSearchTool()
```

```python
# Google API toolsets: get Workspace tools and pass to an agent.
from google.adk.tools.google_api_tool import GmailToolset

gmail_toolset = GmailToolset()
gmail_tools = gmail_toolset.get_tools()
```

```python
# Google Cloud database toolsets: expose DB tools.
from google.adk.tools.bigquery import BigQueryToolset

bq_toolset = BigQueryToolset()
bq_tools = bq_toolset.get_tools()
```

```python
# Memory and artifacts tools: query memory or artifacts in tools.
from google.adk.tools import LoadMemoryTool, LoadArtifactsTool, UrlContextTool

tools = [LoadMemoryTool(), LoadArtifactsTool(), UrlContextTool()]
```

## Context Types (Where You Read/Write State)

- `InvocationContext`: Full context for a single invocation; includes session, services, run config.
- `ReadonlyContext`: Read-only view of context; used for instruction providers.
- `CallbackContext`: Used in callbacks; can read/write `state` and work with artifacts.
- `ToolContext`: Used in tools; can read/write `state`, request auth, search memory, manage artifacts.
- `LiveRequest` and `LiveRequestQueue`: Streaming input types for live/real-time runs.

## Sessions, State, and Memory

- `Session`: A single conversation thread with `id`, `state`, and `events`.
- `SessionService`: Manages session lifecycle and persistence.
  - `InMemorySessionService`, `DatabaseSessionService`, `VertexAiSessionService`.
- `State` (`session.state`): Scratchpad for the current session, updated via events.
  - Prefix scopes: `user:`, `app:`, `temp:`.
- `MemoryService`: Long-term, searchable knowledge store.
  - `InMemoryMemoryService`, `VertexAiMemoryBankService`.

## Events and Actions

- `Event`: Immutable record for each step (user input, model output, tool call/response, errors).
- `EventActions`: Holds side effects and control signals.
  - `state_delta`, `artifact_delta`, `transfer_to_agent`, `escalate`, `skip_summarization`.

## Artifacts

- `BaseArtifactService`: Interface for artifact storage.
- `InMemoryArtifactService`: In-memory artifacts.
- `GcsArtifactService`: Artifact storage in GCS.
- Artifacts are saved/loaded via context (`save_artifact`, `load_artifact`) and tracked in events.

## Runtime and Runners

- `Runner`: Orchestrates an invocation, processes events, and commits state.
- `InMemoryRunner`: Convenience runner using in-memory services.
- `RunConfig`: Runtime configuration (streaming, modalities, max LLM calls, audio transcriptions).

## Apps and Resumability

- `App`: Top-level container for an agent, plugins, and configs.
- `ResumabilityConfig`: Controls whether sessions/invocations are resumable.

## Callbacks and Plugins

- Agent callbacks: `before_agent_callback`, `after_agent_callback`.
- Model callbacks: `before_model_callback`, `after_model_callback`.
- Tool callbacks: `before_tool_callback`, `after_tool_callback`.
- `BasePlugin`: Centralized way to register callbacks and system hooks.
- `PluginManager`: Registers plugins and executes their callbacks.
- `LoggingPlugin`, `ReflectAndRetryToolPlugin`: Built-in plugin examples.

## Useful Supporting Types

- `InvocationContext` fields: `session`, `session_service`, `memory_service`, `artifact_service`, `run_config`.
- `ToolContext` helpers: `request_credential`, `request_confirmation`, `search_memory`.
