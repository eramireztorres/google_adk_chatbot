import subprocess, shlex, os
from typing import Optional, Dict, Any

def run_shell(command: str, workdir: Optional[str] = None, timeout: int = 180) -> Dict[str, Any]:
    """
    Runs a shell command. Deletion attempts are blocked by the agent's before_tool_callback.
    """
    cwd = workdir or os.getcwd()
    try:
        proc = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {"ok": True, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    except subprocess.TimeoutExpired as e:
        return {"ok": False, "returncode": None, "stdout": e.stdout or "", "stderr": f"Timeout: {e}"}
