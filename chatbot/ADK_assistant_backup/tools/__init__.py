"""Tool wrappers for ADK agents."""

from google.adk.tools import FunctionTool

from .file_tool import list_dir, read_file, write_file, create_file
from .shell_tool import run_shell
from .code_sanity_tool import code_sanity_check
from .import_check_tool import import_check

file_tools = [
    FunctionTool(func=list_dir),
    FunctionTool(func=read_file),
    FunctionTool(func=write_file),
    FunctionTool(func=create_file),
]

shell_tools = [FunctionTool(func=run_shell)]

sanity_tools = [FunctionTool(func=code_sanity_check), FunctionTool(func=import_check)]

__all__ = [
    "file_tools",
    "shell_tools",
    "sanity_tools",
    "list_dir",
    "read_file",
    "write_file",
    "create_file",
    "run_shell",
    "code_sanity_check",
    "import_check",
]
