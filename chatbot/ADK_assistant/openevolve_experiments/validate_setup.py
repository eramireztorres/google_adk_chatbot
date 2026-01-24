import sys
import os
import importlib.util
import subprocess
import time
import requests

MCP_SERVER_SCRIPT = "/home/erick/repo/google_adk_chatbot/rag/run_adk_mcp_server.py"
ENV_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
VENV_PYTHON = "/home/erick/repo/google_adk_chatbot/venv/bin/python"

def wait_for_server(url, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
           # Assuming MCP server has a health check or just listening on port
           # The MCP server might just be an SSE endpoint, let's try to connect
           # Note: Typical MCP SSE endpoints might not respond to GET / with 200, but connection refused means it's down.
           requests.get(url, timeout=1)
           return True
        except requests.ConnectionError:
            time.sleep(0.5)
        except Exception:
            # If we get a 404 or something, the server is UP at least.
            return True
    return False

def validate():
    print("Validating setup...")
    
    # Check if files exist
    files = ["evaluator.py", "config.yaml", "initial_program.py", ".env"]
    for f in files:
        if not os.path.exists(f):
             sys.exit(f"❌ '{f}' missing")
    print("Files found.")
    
    # Start MCP Server
    print("Starts MCP Server...")
    # Load env vars for subprocess
    env = os.environ.copy()
    # Read .env manually to pass to subprocess? Or trust that subprocess inherits execution env?
    # Better to source .env or use python-dotenv. 
    # But for simplicity, let's assume valid runtime or just pass the envs if we read them.
    # Actually, we can just run the server using the venv python, and it should pick up standard things? 
    # But the user said .env has the keys. We should load them.
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE, override=True)
    env = os.environ.copy() # Update env with loaded vars

    server_proc = subprocess.Popen(
        [VENV_PYTHON, MCP_SERVER_SCRIPT, "--host", "127.0.0.1"], 
        env=env,
        stdout=None, # Inherit stdout
        stderr=None  # Inherit stderr
    )
    
    # Wait for server
    print("Waiting for MCP server to start...")
    if not wait_for_server("http://127.0.0.1:8000/sse"):
         print("❌ MCP server failed to respond.")
         server_proc.terminate()
         sys.exit(1) 
    
    if server_proc.poll() is not None:
         print("❌ MCP server failed to start.")
         print(server_proc.stderr.read().decode())
         sys.exit(1)
         
    print("MCP Server running (pid={})".format(server_proc.pid))

    try:
        # Import evaluator
        spec = importlib.util.spec_from_file_location("evaluator", "evaluator.py")
        eval_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(eval_module)
    
        # Run evaluation on initial_program.py
        print("Running evaluation on initial_program.py...")
        res = eval_module.evaluate(os.path.abspath("initial_program.py"))
        print(f"Result: {res}")
        if isinstance(res, dict) and "artifacts" in res:
             print(f"Artifacts: {res['artifacts']}")
        
        if isinstance(res, dict):
            if "error" in res:
                raise ValueError(f"Evaluator returned error: {res['error']}")
            score = res.get("combined_score")
        else: 
            score = res.metrics.get("combined_score")
            
        if score is None: 
            raise ValueError("No combined_score in result")
            
        print("✅ Setup Valid")
    except Exception as e:
        print(f"❌ Validation Failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Stopping MCP server...")
        server_proc.terminate()
        server_proc.wait()

if __name__ == "__main__":
    validate()
