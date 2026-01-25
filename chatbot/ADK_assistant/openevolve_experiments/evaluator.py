import importlib.util
import json
import logging
import os
import re
import subprocess
import sys
import time
import asyncio
import uuid
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
VENV_PYTHON = "/home/erick/repo/google_adk_chatbot/venv/bin/python"
QUERIES_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../rag_test_queries.json"))
ENV_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))

# Load environment variables explicitly, safely not overriding existing env vars
load_dotenv(ENV_FILE, override=False)

def run_python_code(code: str) -> Dict[str, Any]:
    """Runs the provided Python code using the specified virtual environment."""
    if not code or not code.strip():
        return {"success": False, "out": "", "err": "No code provided"}

    import tempfile
    
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        temp_path = f.name

    try:
        # Run with timeout
        result = subprocess.run(
            [VENV_PYTHON, temp_path],
            capture_output=True,
            text=True,
            timeout=15 
        )
        return {
            "success": result.returncode == 0,
            "out": result.stdout,
            "err": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "out": "", "err": "Execution timed out", "returncode": -1}
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass

def extract_python_code(text: str) -> Optional[str]:
    """Extracts the first Python code block from the text."""
    match = re.search(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return None

async def run_query(root_agent, query: str) -> Dict[str, Any]:
    """Runs a single query against the agent using the Runner pattern."""
    from google.adk import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    start_time = time.time()
    response_text = ""
    
    try:
        session_service = InMemorySessionService()
        # Initialize session explicitly
        session_id = str(uuid.uuid4())
        session_service.create_session_sync(app_name="TestApp", session_id=session_id, user_id="test_user")
        
        runner = Runner(agent=root_agent, session_service=session_service, app_name="TestApp")
        
        # Correctly iterate over async generator events
        async for event in runner.run_async(
            user_id="test_user", 
            session_id=session_id, 
            new_message=types.Content(parts=[types.Part(text=query)])
        ):
             if hasattr(event, "content") and event.content:
                 if isinstance(event.content, str):
                     response_text += event.content
                 elif hasattr(event.content, "parts"):
                     for part in event.content.parts:
                         if part.text:
                             response_text += part.text
                             
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        response_text = f"Error: {str(e)}"

    latency = time.time() - start_time
    return {
        "response": response_text,
        "latency": latency
    }


def evaluate(program_path: str) -> Dict[str, Any]:
    """Evaluates the candidate program."""
    try:
        # 1. Import module dynamicallly
        spec = importlib.util.spec_from_file_location("candidate", program_path)
        if spec is None or spec.loader is None:
            return {"combined_score": 0.0, "error": "Could not load spec"}
        candidate_module = importlib.util.module_from_spec(spec)
        sys.modules["candidate"] = candidate_module 
        spec.loader.exec_module(candidate_module)

        if not hasattr(candidate_module, "root_agent"):
             return {"combined_score": 0.0, "error": "candidate has no root_agent"}

        root_agent = candidate_module.root_agent

        # 2. Load queries
        if not os.path.exists(QUERIES_FILE):
             return {"combined_score": 0.0, "error": f"Queries file not found at {QUERIES_FILE}"}
             
        with open(QUERIES_FILE, "r") as f:
            test_cases = json.load(f)

        total_score = 0.0
        details = []
        total_latency = 0.0
        
        # 3. Run evaluation loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        valid_cases = 0

        for case in test_cases:
            query = case["query"]
            keywords = case.get("keywords", [])
            
            run_res = loop.run_until_complete(run_query(root_agent, query))
            
            response = run_res["response"]
            latency = run_res["latency"]
            total_latency += latency
            
            code = extract_python_code(response)
            
            code_exec_success = False
            keyword_score = 0
            
            if code:
                exec_res = run_python_code(code)
                code_exec_success = exec_res["success"]
            
            search_text = code if code else response 
            
            hits = 0
            if keywords:
                for k in keywords:
                    if k in search_text:
                        hits += 1
                keyword_score = hits / len(keywords)

            case_score = 0.0
            if code:
                case_score += 0.4
                if code_exec_success:
                    case_score += 0.3
            case_score += 0.3 * keyword_score
            
            total_score += case_score
            valid_cases += 1
            
            details.append({
                "query": query,
                "score": case_score,
                "latency": latency,
                "code_extracted": bool(code),
                "exec_success": code_exec_success,
                "keyword_match": keyword_score
            })
            
        # Cleanup pending tasks to avoid "Task was destroyed" errors
        try:
            pending = asyncio.all_tasks(loop)
            if pending:
                for task in pending:
                    task.cancel()
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception:
            pass # Ignore errors during cleanup
            
        loop.close()

        if valid_cases == 0:
            return {"combined_score": 0.0, "error": "No valid test cases run"}

        avg_score = total_score / valid_cases
        avg_latency = total_latency / valid_cases
        
        # User requested small weight without threshold (to avoid zeroing score on high latency)
        latency_penalty = avg_latency * 0.001 
        
        final_score = avg_score - latency_penalty

        return {
            "combined_score": final_score,
            "latency": avg_latency,
            "artifacts": {
                "details": details, 
                "avg_latency": avg_latency
            }
        }

    except Exception as e:
        import traceback
        return {
            "combined_score": 0.0, 
            "error": str(e),
            "artifacts": {"traceback": traceback.format_exc()}
        }
