from __future__ import annotations

import os
import shlex
from pathlib import Path
from typing import Any, Dict, Optional

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from ..config.settings import get_settings

_FILE_TOOL_NAMES = {"read_file", "write_file", "list_dir", "create_file"}
_SHELL_TOOL_NAMES = {"run_shell"}


def _is_within_base(path: str, base_dir: str) -> bool:
    if not os.path.isabs(path):
        path = os.path.join(base_dir, path)
    resolved = Path(path).resolve()
    base = Path(base_dir).resolve()
    return resolved == base or str(resolved).startswith(str(base) + os.sep)


def before_tool_guardrails(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict[str, Any]]:
    settings = get_settings()
    tool_name = tool.name

    if tool_name in _FILE_TOOL_NAMES:
        target = args.get("path", "")
        if not target:
            return {"ok": False, "error": "Missing path."}
        if not _is_within_base(target, settings.base_dir):
            return {"ok": False, "error": "Path outside allowed workspace."}
        return None

    if tool_name in _SHELL_TOOL_NAMES:
        command = args.get("command", "")
        if not command:
            return {"ok": False, "error": "Missing command."}
        try:
            first = shlex.split(command)[0]
        except Exception:
            return {"ok": False, "error": "Invalid command."}
        if first not in settings.allowed_shell_commands:
            return {"ok": False, "error": f"Command '{first}' not allowed."}
        return None

    return None
