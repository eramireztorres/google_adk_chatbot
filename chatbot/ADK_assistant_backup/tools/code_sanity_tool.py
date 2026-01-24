from __future__ import annotations

import ast
import importlib.util
import re
from typing import Dict, List

from google.adk.tools.tool_context import ToolContext

_CODE_FENCE_RE = re.compile(r"```(?:python)?\n(.*?)\n```", re.DOTALL)


def _extract_code(text: str) -> str:
    matches = _CODE_FENCE_RE.findall(text)
    if matches:
        return "\n\n".join(match.strip() for match in matches if match.strip())
    return text.strip()


def _collect_imports(tree: ast.AST) -> List[str]:
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return sorted(set(imports))


def code_sanity_check(code: str, tool_context: ToolContext) -> Dict[str, object]:
    """
    Parse code and check for syntax/import issues without executing user code.
    Returns warnings for missing modules instead of failing hard.
    """
    snippet = _extract_code(code)
    if not snippet:
        return {"ok": False, "error": "No code provided."}

    try:
        tree = ast.parse(snippet)
    except SyntaxError as exc:
        return {"ok": False, "error": f"SyntaxError: {exc}"}

    missing = []
    for name in _collect_imports(tree):
        if name.startswith("."):
            continue
        if importlib.util.find_spec(name) is None:
            missing.append(name)

    result = {
        "ok": True,
        "missing_modules": missing,
    }
    if missing:
        result["warning"] = "Some imports are missing in this environment."

    tool_context.state["code_sanity:last_result"] = result
    return result
