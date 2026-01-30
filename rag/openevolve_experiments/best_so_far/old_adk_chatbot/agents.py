from typing import Optional, Dict, List, Any
import re
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools import BaseTool, ToolContext
from google.genai import types

# from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

# --- Tools ---

def say_hello(name: Optional[str] = None) -> str:
    """Provides a friendly greeting."""
    if name:
        return f"Hello, {name}! How can I help you with AdK today?"
    return "Hello! I am your AdK Assistant. How can I help you?"

def say_goodbye() -> str:
    """Provides a polite farewell."""
    return "Goodbye! Happy coding with AdK."

# --- Callbacks ---

def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Safety guardrail to block requests containing 'BLOCK'."""
    last_user_msg = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            # Content might be a string or an object with role
            # Robustly check for text content regardless of object type
            if isinstance(content, str):
                 last_user_msg = content
                 break
            
            try:
                if hasattr(content, "role") and content.role == 'user' and hasattr(content, "parts") and content.parts:
                    if content.parts[0].text:
                        text = content.parts[0].text
                        # Skip AdK context messages
                        if text.startswith("For context:"):
                            continue
                            
                        last_user_msg = text
                        break
            except Exception:
                continue
    
    if "BLOCK" in last_user_msg.upper():
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="I cannot process this request due to safety guidelines.")]
            )
        )
    return None

# --- Tool Guardrails ---

_INJECTION_PATTERNS = [
    r"ignore (all|previous|prior) instructions",
    r"disregard (all|previous|prior) instructions",
    r"reveal (the )?system prompt",
    r"show (the )?developer message",
    r"print (the )?hidden prompt",
    r"jailbreak",
]


def _looks_like_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in _INJECTION_PATTERNS)


def validate_rag_tool_call(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
) -> Optional[Dict[str, Any]]:
    """Block risky or malformed tool calls before execution."""
    query = args.get("query") or args.get("question")
    if not query or not isinstance(query, str) or not query.strip():
        return {"error": "Tool call blocked: missing query text."}

    if len(query) > 1000:
        return {"error": "Tool call blocked: query too long."}

    if _looks_like_prompt_injection(query):
        return {"error": "Tool call blocked: suspected prompt injection."}

    return None

# --- Agents ---

# Model constant - can be swapped easily
MODEL_NAME = LiteLlm(model="openai/gpt-4.1-mini") # Switched to OpenAI GPT-4.1 Mini per request

def create_agent_team() -> Agent:
    """Creates and configures the agent team, returning the Root Agent."""
    
    # Create MCP Toolset for RAG
    # Note: connect synchronously definition, but runtime connection is handled by AdK
    rag_tools = McpToolset(
        connection_params=SseConnectionParams(
            url="http://localhost:8000/sse",
        )
    )

    # Callback to inspect RAG output
    def log_rag_output(
        tool: BaseTool,
        args: Dict[str, Any],
        tool_context: ToolContext,
        tool_response: Dict,
    ) -> Optional[Dict]:
        print(f"\n[DEBUG] RAG Tool Output ({tool.name}):")
        print(tool_response)
        return None

    rag_agent = Agent(
        model=MODEL_NAME,
        name="rag_agent",
        instruction="You are the AdK Knowledge Specialist. Always call the MCP tool `get_adk_info` for ADK questions. "
                    "Return only the tool's `answer` field as plain text. Do not include JSON or `contexts` in the reply. "
                    "Only use information present in the tool's contexts. "
                    "If the user requests code/examples/snippets and the tool's contexts do not include code, reply "
                    "\"Not found in the provided documentation.\" "
                    "If the tool answer says \"Not found in the provided documentation.\", ask a brief clarifying question. "
                    "Do not guess imports or APIs.",
        description="Handles technical questions about Google AdK framework, agents, tools, etc.",
        tools=[rag_tools],
        after_tool_callback=log_rag_output,
        before_tool_callback=validate_rag_tool_call,
    )

    # Root Agent (Orchestrator)
    root_agent = Agent(
        model=MODEL_NAME,
        name="root_agent",
        instruction="You are the Lead AdK Chatbot. Route requests carefully based on intent and conversation state.\n"
                    "- If the user asks about Google ADK, tools, agents, APIs, or requests examples/code, delegate to rag_agent.\n"
                    "- If the user says a short follow-up like \"yes\", \"please\", \"show code\", or \"more\", treat it as a continuation\n"
                    "  of the last ADK-related question and delegate to rag_agent.\n"
                    "- If the user greets you, respond using say_hello.\n"
                    "- If the user says goodbye, respond using say_goodbye.\n"
                    "- If intent is unclear, ask a brief clarification question.\n"
                    "Always maintain conversation continuity and never reset to a greeting mid-thread.",
        description="Main coordinator.",
        sub_agents=[rag_agent],
        tools=[say_hello, say_goodbye],
        before_model_callback=block_keyword_guardrail,
    )
    
    return root_agent
