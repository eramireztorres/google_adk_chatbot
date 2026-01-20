# Google ADK Types and Classes Cheat Sheet

A comprehensive reference guide for the Google Agent Development Kit (ADK) types and classes, organized by functional areas.

---

## 1. Agent Types

### 1.1 LLM Agents

**`LlmAgent` (alias: `Agent`)**
The core agent type that uses Large Language Models for reasoning and decision-making.

**Key Parameters:**
- `name` (required): Unique identifier for the agent
- `model` (required): LLM model identifier (e.g., "gemini-2.0-flash")
- `instruction`: Core guidance for agent behavior
- `description`: Helps other agents understand this agent's capabilities
- `tools`: List of tools the agent can use
- `generate_content_config`: LLM generation parameters (temperature, max_tokens, etc.)
- `input_schema`/`output_schema`: Define structured input/output
- `output_key`: Store response in session state
- `include_contents`: Control conversation history (`'default'` or `'none'`)
- `planner`: Enable multi-step reasoning (BuiltInPlanner, PlanReActPlanner)
- `code_executor`: Allow code execution in responses

**Callbacks:**
- `before_agent_callback` / `after_agent_callback`
- `before_model_callback` / `after_model_callback`
- `before_tool_callback` / `after_tool_callback`

---

### 1.2 Workflow Agents

**`SequentialAgent`**
Executes sub-agents one after another in sequence.

**Use Case:** Multi-step processes where each step depends on the previous one.

---

**`ParallelAgent`**
Executes multiple sub-agents concurrently.

**Use Case:** Independent tasks that can run simultaneously for efficiency.

---

**`LoopAgent`**
Repeatedly executes sub-agents until a termination condition is met.

**Use Case:** Iterative processes, retry logic, refinement loops.

**Termination:** Via `actions.escalate = True` in tools/callbacks.

---

### 1.3 Custom Agents

**`BaseAgent`**
Abstract base class for creating custom agents with specialized behavior.

**Key Methods to Implement:**
- `_run_async_impl(ctx: InvocationContext)`: Core agent logic
- `_run_live_impl(ctx: InvocationContext)`: For live/streaming scenarios

**Use Case:** Agents with deterministic logic, custom orchestration, or non-LLM-based decision-making.

---

## 2. Tool Types

### 2.1 Function Tools

**`FunctionTool`**
Wraps Python functions/methods as tools that agents can call.

**Best Practices:**
- Use descriptive function names (verb-noun pattern)
- Provide type hints for all parameters
- Write clear docstrings (used by LLM to understand tool)
- Return `dict` objects with descriptive keys
- Include `status` key in returns (e.g., 'success', 'error')

**Example:**
```python
def get_weather(city: str) -> dict:
    """Retrieves weather for a city."""
    return {"status": "success", "temperature": "25°C"}
```

---

**`AgentTool`**
Uses another agent as a tool for delegation.

**Use Case:** Multi-agent systems, specialized sub-agents.

---

**`LongRunningTool`**
For tools that perform asynchronous operations or take significant time.

**Key Parameter:**
- `is_long_running=True`

---

### 2.2 Built-in Tools

- **Google Search**: Web search integration
- **Code Execution**: Execute code in LLM responses
- **RAG Tools**: Retrieval-Augmented Generation

---

### 2.3 External Tool Types

**`RestApiTool`**
Call REST API endpoints.

---

**`OpenAPITool`**
Auto-generate tools from OpenAPI specifications.

---

**`MCPTool`**
Model Context Protocol tools for standardized integrations.

---

### 2.4 Toolsets

**`BaseToolset`**
Group and dynamically provide collections of tools.

**Key Methods:**
- `async get_tools(readonly_context) -> list[BaseTool]`
- `async close()`: Cleanup resources

**Use Case:** Organizing related tools, dynamic tool availability based on context.

---

## 3. Context Types

### 3.1 InvocationContext

**Access:** Passed to agent's `_run_async_impl` method.

**Contains:**
- Full invocation state
- `session` (including state and events)
- `agent` instance
- `invocation_id`
- `user_content`
- Service references (artifact_service, memory_service, session_service)

**Use Case:** Direct agent implementation, controlling invocation lifecycle.

---

### 3.2 ReadonlyContext

**Access:** Provided to instruction providers, base for other contexts.

**Contains:**
- `invocation_id`
- `agent_name`
- Read-only view of `state`

**Use Case:** Safe read-only access to basic contextual information.

---

### 3.3 CallbackContext

**Access:** Passed to agent and model callbacks.

**Capabilities (extends ReadonlyContext):**
- Mutable `state` property (read/write)
- `load_artifact(filename)` / `save_artifact(filename, part)`
- `user_content` access

**Use Case:** Inspecting and modifying state, managing artifacts within callbacks.

---

### 3.4 ToolContext

**Access:** Passed to tool functions and tool callbacks.

**Capabilities (extends CallbackContext):**
- All CallbackContext features
- `request_credential(auth_config)`: Trigger auth flow
- `get_auth_response(auth_config)`: Retrieve credentials
- `list_artifacts()`: Discover available artifacts
- `search_memory(query)`: Query memory service
- `function_call_id`: Unique identifier for this tool invocation
- `actions`: Direct access to EventActions

**Use Case:** Advanced tool operations, authentication, memory search, state management.

---

## 4. Events and Event Components

### 4.1 Event

**Purpose:** Fundamental unit of information flow in ADK.

**Key Fields:**
- `author`: 'user' or agent name
- `invocation_id`: ID for the entire interaction
- `id`: Unique event ID
- `content`: Message payload (text, function calls/responses)
- `actions`: Side effects and control signals (EventActions)
- `partial`: Indicates streaming chunk
- `turn_complete`: Marks end of a turn
- `timestamp`: Creation time

**Helper Methods:**
- `is_final_response()`: Identifies displayable final responses
- `get_function_calls()`: Extract tool call requests
- `get_function_responses()`: Extract tool results

---

### 4.2 EventActions

**Purpose:** Signal state changes and control flow within events.

**Key Fields:**
- `state_delta`: Dict of state changes
- `artifact_delta`: Dict of artifact updates
- `transfer_to_agent`: Transfer control to named agent
- `escalate`: Signal loop termination
- `skip_summarization`: Skip LLM summarization of tool result
- `requested_auth_configs`: Authentication requests

---

### 4.3 LlmRequest

**Purpose:** Represents a request to the LLM.

**Key Fields:**
- `contents`: Conversation history
- `config`: GenerateContentConfig
- `tools`: Available tools

---

### 4.4 LlmResponse

**Purpose:** Response from the LLM.

**Key Fields:**
- `content`: Generated content
- `partial`: Streaming indicator
- `error_code` / `error_message`: Error information

---

## 5. Session Management

### 5.1 Session

**Purpose:** Container for a single conversation thread.

**Key Components:**
- `id`: Session identifier
- `user_id`: User identifier
- `app_name`: Application name
- `state`: Session state dictionary
- `events`: Chronological event history

**State Prefixes:**
- `app:key`: Application-wide state
- `user:key`: User-specific across sessions
- `temp:key`: Temporary, invocation-scoped
- `key`: Session-specific

---

### 5.2 State

**Purpose:** Dictionary-like storage for session data.

**Operations:**
- Read: `state['key']` or `state.get('key', default)`
- Write: `state['key'] = value`
- Changes tracked via `state_delta` in events

---

### 5.3 Session Service Types

**`BaseSessionService`**
Abstract interface for session persistence.

---

**`InMemorySessionService`**
In-memory storage for testing/development.
**Warning:** Data lost on application restart.

---

**`DatabaseSessionService`**
Persistent database-backed storage.

---

**`VertexAiSessionService`**
Google Cloud Vertex AI integration.

**Key Methods:**
- `create_session()`: Create new session
- `get_session()`: Retrieve existing session
- `append_event()`: Add event and apply state changes
- `delete_session()`: Remove session

---

## 6. Memory and Artifacts

### 6.1 Memory Services

**`BaseMemoryService`**
Abstract interface for long-term memory across sessions.

**Key Methods:**
- `search_memory(query)`: Search stored knowledge
- `ingest()`: Store information

**Use Case:** Cross-session knowledge, user preferences, past interactions.

---

### 6.2 Artifact Services

**`BaseArtifactService`**
Abstract interface for file/blob storage.

---

**`InMemoryArtifactService`**
In-memory artifact storage.

---

**`GcsArtifactService`**
Google Cloud Storage backend.

**Key Methods:**
- `save(filename, part)`: Store artifact
- `load(filename, version)`: Retrieve artifact
- `list()`: List available artifacts

**Use Case:** Managing files (PDFs, images, documents) associated with sessions.

---

## 7. Runtime Components

### 7.1 Runner

**Purpose:** Main orchestrator for agent execution.

**Key Methods:**
- `run_async(user_id, session_id, new_message)`: Execute agent (async)
- `run(user_id, session_id, new_message)`: Execute agent (sync wrapper)

**Responsibilities:**
- Manages event loop
- Processes events from agents
- Commits state/artifact changes via services
- Forwards events to application

**Configuration:**
- `agent`: Root agent to execute
- `app_name`: Application identifier
- `session_service`: Session management
- `artifact_service`: Artifact management (optional)
- `memory_service`: Memory management (optional)

---

### 7.2 RunConfig

**Purpose:** Configuration for agent execution.

**Key Parameters:**
- `streaming_mode`: Control streaming behavior
- `max_turns`: Limit conversation turns
- `timeout`: Execution timeout

---

## 8. Model Types

### 8.1 Google Gemini Models

**Direct String Usage:**
```python
model="gemini-2.0-flash"
model="gemini-2.5-pro-preview-03-25"
```

**Authentication:**
- Google AI Studio: API Key via `GOOGLE_API_KEY`
- Vertex AI: ADC, Service Account, or Express Mode

**Environment Variables:**
- `GOOGLE_GENAI_USE_VERTEXAI=TRUE/FALSE`
- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_CLOUD_LOCATION`

---

### 8.2 Claude (Anthropic)

**`Claude` Wrapper Class**

**Direct API:**
```python
model=Claude(model_id, anthropic_client)
```

**Vertex AI:**
```python
# Python: Register and use string
LLMRegistry.register(Claude)
model="claude-3-sonnet@20240229"
```

---

### 8.3 LiteLLM Integration

**`LiteLlm` Wrapper Class**

**Purpose:** Access 100+ LLMs via unified interface.

**Examples:**
```python
model=LiteLlm(model="openai/gpt-4o")
model=LiteLlm(model="anthropic/claude-3-haiku-20240307")
model=LiteLlm(model="ollama_chat/mistral-small3.1")
```

**Configuration:**
- Provider API keys via environment variables
- `api_base` for custom endpoints
- `extra_headers` for authentication

---

### 8.4 Apigee Gateway

**`ApigeeLlm` Wrapper Class**

**Purpose:** Route AI traffic through Apigee for governance.

**Features:**
- Model safety (Model Armor)
- Rate/token limiting
- Semantic caching
- Monitoring and analytics

**Example:**
```python
model=ApigeeLlm(
    model="apigee/gemini-2.5-flash",
    proxy_url="https://your-apigee-proxy-url",
    custom_headers={"auth": "key"}
)
```

---

## 9. Callbacks

### 9.1 Agent Lifecycle Callbacks

**`before_agent_callback`**
- **When:** Before agent's main execution
- **Context:** CallbackContext
- **Return:** `types.Content` to skip agent execution, `None` to proceed

---

**`after_agent_callback`**
- **When:** After agent completes
- **Context:** CallbackContext
- **Return:** `types.Content` to replace agent output, `None` to use original

---

### 9.2 Model Interaction Callbacks

**`before_model_callback`**
- **When:** Before LLM call
- **Context:** CallbackContext
- **Parameters:** LlmRequest
- **Return:** `LlmResponse` to skip LLM call, `None` to proceed

**Use Cases:** Guardrails, prompt validation, caching.

---

**`after_model_callback`**
- **When:** After LLM responds
- **Context:** CallbackContext
- **Parameters:** LlmResponse
- **Return:** `LlmResponse` to replace output, `None` to use original

**Use Cases:** Output sanitization, adding disclaimers.

---

### 9.3 Tool Execution Callbacks

**`before_tool_callback`**
- **When:** Before tool execution
- **Context:** ToolContext
- **Return:** `dict` to skip tool execution, `None` to proceed

**Use Cases:** Validation, policy enforcement, mocking.

---

**`after_tool_callback`**
- **When:** After tool executes
- **Context:** ToolContext
- **Return:** `dict` to replace tool result, `None` to use original

**Use Cases:** Result post-processing, standardization.

---

## 10. Planners

### 10.1 BasePlanner

**Purpose:** Abstract interface for multi-step reasoning.

---

### 10.2 BuiltInPlanner

**Purpose:** Leverages model's built-in planning (e.g., Gemini thinking).

**Configuration:**
```python
planner=BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_budget=1024
    )
)
```

**Use Case:** Models with native planning/thinking features.

---

### 10.3 PlanReActPlanner

**Purpose:** Structured plan-then-act approach.

**Output Format:**
```
/*PLANNING*/
[steps...]

/*ACTION*/
[tool calls...]

/*REASONING*/
[justification...]

/*FINAL_ANSWER*/
[response...]
```

**Use Case:** Models without built-in thinking, explicit reasoning traces.

---

## 11. Configuration and Schema Types

### 11.1 GenerateContentConfig

**Purpose:** Configure LLM generation parameters.

**Key Parameters:**
- `temperature`: Randomness (0.0-1.0)
- `max_output_tokens`: Response length limit
- `top_p` / `top_k`: Sampling parameters
- `safety_settings`: Content filtering
- `http_options`: Retry configuration

---

### 11.2 Schema (Input/Output)

**Purpose:** Define structured data formats.

**Types:**
- Python: Pydantic `BaseModel`
- Go: `genai.Schema`
- Java: `Schema` builder

**Usage:**
- `input_schema`: Enforce input format
- `output_schema`: Enforce output format (JSON)

**Note:** Output schema prevents tool use.

---

### 11.3 AuthConfig

**Purpose:** Configure authentication for tools.

**Methods:**
- `request_credential(auth_config)`: Initiate auth flow
- `get_auth_response(auth_config)`: Retrieve credentials

**Use Case:** Tools requiring API keys, OAuth tokens, etc.

---

## 12. Additional Important Types

### 12.1 Content and Parts

**`Content`** (from google.genai.types)
- `role`: 'user', 'model', or 'system'
- `parts`: List of Part objects

**`Part`**
- `text`: Text content
- `function_call`: Tool call request
- `function_response`: Tool result
- `inline_data`: Binary data (images, etc.)

---

### 12.2 Safety and Error Types

**`SafetySetting`**
- `category`: Harm category
- `threshold`: Block threshold

**`HarmCategory`** / **`HarmBlockThreshold`**
Content safety enumerations.

---

### 12.3 Streaming Types

**Streaming Modes:**
- `StreamingModeNone`: No streaming
- `StreamingModeSSE`: Server-sent events
- `StreamingModeLive`: Bidi-streaming

**Live API Features:**
- Real-time audio/video
- Low-latency interaction
- Voice/video streaming models

---

## 13. Best Practices Summary

### Agent Design
- Use clear, specific instructions
- Guide tool usage explicitly in instructions
- Handle different tool return values (success/error)
- Use appropriate agent types (LLM vs Workflow)

### Tool Development
- Descriptive names and docstrings
- Type hints for all parameters
- Return dicts with status indicators
- Keep tools focused (single responsibility)
- Avoid complex nested structures

### State Management
- Use state prefixes appropriately (app:, user:, temp:)
- Understand dirty reads vs committed state
- Track state changes via state_delta
- Persist critical state in events

### Context Usage
- Use most specific context type available
- Modify state only in mutable contexts
- Use artifacts for file management
- Leverage memory for cross-session data

### Event Handling
- Filter events with `is_final_response()`
- Process partial events for streaming
- Check `actions` for state/control signals
- Use `invocation_id` for correlation

### Callbacks
- Return `None` to allow default behavior
- Return specific object type to override
- Use for guardrails, logging, state management
- Consider Plugins for security guardrails

### Error Handling
- Check `error_code` and `error_message` in events
- Handle tool failures gracefully
- Implement retry logic via callbacks or planners
- Use appropriate safety settings

---

## Quick Reference: Common Patterns

### Creating a Basic LLM Agent
```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="my_agent",
    instruction="You are a helpful assistant.",
    tools=[my_tool_function]
)
```

### Running an Agent
```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
runner = Runner(
    agent=agent,
    app_name="my_app",
    session_service=session_service
)

# Async
async for event in runner.run_async(user_id, session_id, user_message):
    if event.is_final_response():
        print(event.content.parts[0].text)
```

### Creating a Tool
```python
def my_tool(param: str, tool_context: ToolContext) -> dict:
    """Tool description for LLM."""
    # Access state
    value = tool_context.state.get('key')

    # Modify state
    tool_context.state['result'] = 'value'

    return {"status": "success", "data": "result"}
```

### Implementing a Callback
```python
def my_callback(
    callback_context: CallbackContext,
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    # Inspect request
    print(f"Agent: {callback_context.agent_name}")

    # Modify request (if mutable)
    # ...

    # Return None to proceed, or LlmResponse to skip
    return None
```

### Sequential Workflow
```python
from google.adk.agents import SequentialAgent

workflow = SequentialAgent(
    name="sequential_workflow",
    sub_agents=[agent1, agent2, agent3]
)
```

### Parallel Workflow
```python
from google.adk.agents import ParallelAgent

workflow = ParallelAgent(
    name="parallel_workflow",
    sub_agents=[agent1, agent2, agent3]
)
```

---

**Version:** Based on Google ADK v0.1.0+ Documentation
**Last Updated:** 2026-01-17
