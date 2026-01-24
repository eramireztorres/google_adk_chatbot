from __future__ import annotations

import ast
import importlib
import re
from typing import Dict, List, Tuple

from google.adk.tools.tool_context import ToolContext

_CODE_FENCE_RE = re.compile(r"```(?:python)?\n(.*?)\n```", re.DOTALL)


def _extract_code(text: str) -> str:
    matches = _CODE_FENCE_RE.findall(text)
    if matches:
        return "\n\n".join(match.strip() for match in matches if match.strip())
    return text.strip()


def _collect_imports(tree: ast.AST) -> Tuple[List[str], List[Tuple[str, str]]]:
    imports = []
    from_imports: List[Tuple[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                for alias in node.names:
                    from_imports.append((node.module, alias.name))
    return sorted(set(imports)), sorted(set(from_imports))


def import_check(code: str, tool_context: ToolContext) -> Dict[str, object]:
    """
    Extract Python imports from code and attempt to import them.
    Returns errors instead of executing user code.
    """
    snippet = _extract_code(code)
    if not snippet:
        result = {"ok": False, "error": "No code provided.", "missing_modules": []}
        tool_context.state["import_check:last_result"] = result
        return result

    try:
        tree = ast.parse(snippet)
    except SyntaxError as exc:
        result = {"ok": False, "error": f"SyntaxError: {exc}", "missing_modules": []}
        tool_context.state["import_check:last_result"] = result
        return result

    missing = []
    errors = []
    missing_symbols = []
    imports, from_imports = _collect_imports(tree)

    for name in imports:
        if name.startswith("."):
            continue
        try:
            importlib.import_module(name)
        except ModuleNotFoundError:
            missing.append(name)
        except Exception as exc:
            errors.append(f"{name}: {exc}")

    for module, symbol in from_imports:
        if module.startswith("."):
            continue
        try:
            mod = importlib.import_module(module)
            # Try module.symbol as submodule first, then attribute fallback.
            try:
                importlib.import_module(f"{module}.{symbol}")
            except ModuleNotFoundError:
                if not hasattr(mod, symbol):
                    missing_symbols.append(f"{module}.{symbol}")
        except ModuleNotFoundError:
            missing.append(module)
        except Exception as exc:
            errors.append(f"{module}: {exc}")

    result = {
        "ok": not missing and not errors and not missing_symbols,
        "imports_checked": imports,
        "missing_modules": missing,
        "missing_symbols": missing_symbols,
        "errors": errors,
    }
    if not imports:
        result["ok"] = True
        result["skipped"] = True

    tool_context.state["import_check:last_result"] = result
    return result
