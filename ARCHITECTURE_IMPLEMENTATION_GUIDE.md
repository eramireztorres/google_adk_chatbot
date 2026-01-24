# Google ADK Agent-Team Chatbot Architecture (Implementation Guide)

This document is a step-by-step guide for implementing a Google ADK agent-team chatbot that:

1. Answers questions about Google ADK using the RAG MCP server.
2. Creates new Google ADK projects based on user requirements.

It is written to be executed by an autonomous LLM agent. Follow the steps in order.

---

## 0) Scope, Goals, and Non-Goals

### Goals
- Build a **hybrid multi-agent system** with:
  - **Root coordinator** agent.
  - **RAG Q&A** path with iterative query refinement.
  - **Project creation** path with a sequential pipeline.
  - **Callbacks** for guardrails and tool gating.
- Use the **RAG MCP server** for ADK documentation lookup.
- Ensure **safe tool usage** (file/shell).
- Keep **deterministic checks** outside of LLM logic.

### Non-Goals
- Running all generated code or executing arbitrary tests automatically.
- Full deployment automation (cloud infra, CI/CD).

---

## 1) Project Layout and New Modules

Create the following folders and files:

```
chatbot/
  agent_app.py
  agents/
    __init__.py
    coordinator.py
    rag_qa.py
    project_builder.py
    code_review.py
    safety.py
  callbacks/
    __init__.py
    guardrails.py
    tool_gates.py
    logging.py
  tools/
    __init__.py
    file_tool.py
    shell_tool.py
    code_sanity_tool.py
  config/
    __init__.py
    settings.py
```

Notes:
- Reuse and improve existing tools at:
  - `chatbot/tools/file_tool.py`
  - `chatbot/tools/shell_tool.py`
- Keep **RAG MCP server** as a tool.
- Keep the RAG server separate from the agent runtime.

---

## 2) Global Settings and Environment

### Environment variables
Use `.env` for secrets and model overrides.

```
OPENAI_API_KEY=...
OPENAI_LLM_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TEMPERATURE=0.2
ADK_LLM_PROVIDER=openai
ADK_LLM_MODEL=gpt-4.1-mini
GOOGLE_API_KEY=...
GOOGLE_GENAI_USE_VERTEXAI=FALSE
MCP_PORT=8001
ADK_WEB_PORT=8000
RAG_MCP_URL=http://localhost:8001/sse
```

### Runtime settings (`chatbot/config/settings.py`)
Define:
- MCP server URL (e.g. `http://localhost:8000/sse`)
- Default model(s)
- Tool allowlists
- Filesystem roots (workspace whitelist)
- Max iterations for loops

---

## 3) Callbacks (Guardrails and Tool Gating)

Callbacks should be **small, deterministic, and fast**.
Use them for **guardrails**, **policy enforcement**, **tool gating**, and **logging**.

### 3.1 Guardrails (before_model_callback)
Implement a `before_model_callback` that:
- Detects prompt injection patterns (e.g., “ignore previous instructions”, “act as”, “system prompt”).
- For unsafe prompts, **return a predefined response** and skip LLM call.
- Optionally log to `session.state` for visibility.

### 3.2 Tool gating (before_tool_callback)
Implement a `before_tool_callback` that:
- For file operations, allow only paths inside the repo.
- For shell operations, allow only safe commands (e.g., `rg`, `ls`, `cat`, `python -m pytest`).
- For any disallowed tool call, return a safe error dict and prevent execution.

### 3.3 Logging (after_model_callback, after_tool_callback)
Implement optional lightweight logging callbacks to record:
- Agent name, tool name, and arguments.
- Model usage (model name, token count if available).
- Tool outcomes.

---

## 4) Tools

### 4.1 MCP RAG Tool
Expose the RAG MCP tool to agents:
- Tool name: `get_adk_info`
- Input: `query: str`
- Output: `{answer, contexts, sources}`

### 4.2 File Tool
Implement:
- `read_file(path)`
- `write_file(path, content)`
- `list_dir(path)`

Use **allowlist** based on workspace root.

### 4.3 Shell Tool
Implement a **restricted shell tool**:
- Allow only specific commands.
- No destructive operations.
- No network calls unless explicitly allowed.

### 4.4 Code Sanity Tool
Implement a tool that:
- Extracts python code blocks.
- Runs `ast.parse()` and import checks.
- If missing packages, return **warning**, not failure.
- Never runs arbitrary code.

---

## 5) Agents

### 5.1 Root Coordinator (LLM agent)
Purpose:
- Route between **RAG Q&A** and **Project Creation**.
- Use explicit `AgentTool` or transfer.

Instruction example:
```
You are the coordinator. If the user asks about ADK documentation, route to RAG QA.
If the user asks to create a project or code, route to Project Builder.
```

### 5.2 RAG Q&A Agent (LoopAgent)
Composition:
- `RagQueryAgent` (LLM + MCP tool)
- `RagCriticAgent` (LLM)

Loop behavior:
- Try up to N times.
- Critic rewrites query if answer insufficient.
- Stop when confidence is high or max iterations reached.

### 5.3 Project Builder (SequentialAgent)
Composition:
1. **RequirementsAgent** (LLM) -> state: `requirements`
2. **PlanAgent** (LLM) -> state: `plan`
3. **CodeWriterAgent** (LLM + file tools) -> state: `generated_code`
4. **ADKReviewerAgent** (LLM + RAG MCP tool) -> state: `review_comments`
5. **CodeSanityAgent** (custom/tool) -> state: `sanity_report`

Optional:
- Wrap steps 3–5 in a LoopAgent (max 2–3 iterations).

---

## 6) Integration Steps

1. **Create callback modules** under `chatbot/callbacks/`.
2. **Implement tools** under `chatbot/tools/`.
3. **Define agents** under `chatbot/agents/`.
4. **Wire in callbacks** when creating LLM agents.
5. **Compose agents** into Coordinator + workflow agents.
6. **Expose entrypoint** in `chatbot/agent_app.py`.

---

## 7) Safety and Behavior Rules

- Do not run arbitrary user code.
- Always check file/shell tool calls via callbacks.
- Always use RAG tool for ADK questions.
- For project creation, generate files only after requirements are explicit.
- If dependencies are missing, warn but continue.

---

## 8) Minimal Example Wiring (Pseudo-Outline)

```
root_agent = LlmAgent(
    name="Coordinator",
    sub_agents=[rag_team, project_team],
    tools=[AgentTool(rag_team), AgentTool(project_team)],
    before_model_callbacks=[guardrails_before_model],
)

rag_team = LoopAgent(
    name="RagLoop",
    sub_agents=[rag_query_agent, rag_critic_agent],
    max_iterations=3,
)

project_team = SequentialAgent(
    name="ProjectPipeline",
    sub_agents=[requirements_agent, plan_agent, code_writer_agent, adk_reviewer_agent, sanity_agent],
)
```

---

## 9) Tests (Deterministic)

Focus on:
- Callback rules (blocking/allowing).
- Tool allowlist behavior.
- Code sanity tool parsing.

Use pytest and mock LLM calls.

---

## 10) Deployment and Ops Notes

- Run MCP server separately.
- Keep `.env` with secrets.
- Avoid destructive shell commands.
- Log key events in callbacks.

---

## 11) Future Improvements

- Optional A2A wrapping for the RAG agent if you need remote services.
- Add evaluation harness for Q&A quality.
- Add schema validation for agent outputs.
