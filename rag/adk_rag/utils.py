import re
import ast
import inspect
import importlib
from typing import List, Union, Dict, Any

class PythonCodeExtractor:
    """
    A robust utility to identify and extract Python code snippets from text,
    typically from LLM responses.
    """

    # Regex to match code blocks with optional language tags.
    # It ensures the language tag (if any) and the following newline are not captured.
    _CODE_BLOCK_REGEX = re.compile(
        r"```(?:python3|python|py)?\s*\n?(.*?)```", 
        re.DOTALL | re.IGNORECASE
    )

    @classmethod
    def has_python_code(cls, text: str) -> bool:
        """
        Check if the text contains at least one Python code block.
        
        Args:
            text: The input string to check.
            
        Returns:
            True if at least one code block is found, False otherwise.
        """
        if not text:
            return False
        return bool(cls._CODE_BLOCK_REGEX.search(text))

    @classmethod
    def extract(cls, text: str, join: bool = True) -> Union[str, List[str]]:
        """
        Extract Python code snippets from the text.
        
        Args:
            text: The input string containing potential code blocks.
            join: If True, returns all blocks joined by two newlines. 
                  If False, returns a list of individual code block strings.
                  
        Returns:
            A string containing all extracted code (if join=True) 
            or a list of strings (if join=False).
        """
        if not text:
            return "" if join else []

        matches = cls._CODE_BLOCK_REGEX.findall(text)
        
        # Clean each snippet: strip leading/trailing whitespace
        cleaned_matches = [match.strip() for match in matches if match.strip()]

        if join:
            return "\n\n".join(cleaned_matches)
        return cleaned_matches

    @classmethod
    def extract_robust(cls, text: str) -> str:
        """
        Extracts code snippets and performs basic cleanup to ensure it's as 
        runnable as possible. This is a helper for common LLM extraction patterns.
        """
        code = cls.extract(text, join=True)
        # If no code was found via backticks, we might want to check if the 
        # whole response is just code (heuristic: starts with import or def)
        if not code:
            stripped = text.strip()
            # Simple heuristic: if it looks like code and doesn't have many non-code words
            if stripped.startswith(("import ", "from ", "def ", "class ", "print(")):
                return stripped
        return code


class PythonSnippetChecker:
    """
    Checks Python code snippets for basic errors (imports and class instantiations)
    without running long-running parts or complex logic.
    """

    def __init__(self, code: str):
        self.code = code
        self.execution_globals = {}
        try:
            self.tree = ast.parse(code)
        except SyntaxError as e:
            self.tree = None
            self.syntax_error = str(e)
        else:
            self.syntax_error = None

    def check(self) -> Dict[str, Any]:
        """
        Runs the checks and returns a summary.
        """
        if self.syntax_error:
            return {"success": False, "error": f"Syntax Error: {self.syntax_error}", "stage": "parsing"}

        errors = []
        
        # 1. Execute Imports
        for node in self.tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                try:
                    self._execute_node(node)
                except Exception as e:
                    errors.append(f"Import Error on line {node.lineno}: {e}")

        # 2. Execute likely instantiations
        for node in self.tree.body:
            if isinstance(node, ast.Assign) and self._is_likely_instantiation(node):
                try:
                    self._execute_node(node)
                except Exception as e:
                    errors.append(f"Instantiation Error on line {node.lineno}: {e}")

        if errors:
            return {"success": False, "errors": errors, "stage": "execution"}
        
        return {"success": True, "message": "Imports and instantiations verified successfully."}

    def _is_likely_instantiation(self, node: ast.Assign) -> bool:
        """
        Heuristic to identify ClassName() or module.ClassName() calls.
        """
        if not isinstance(node.value, ast.Call):
            return False
        
        func = node.value.func
        
        # Check by name in globals if possible
        if isinstance(func, ast.Name):
            if func.id in self.execution_globals:
                obj = self.execution_globals[func.id]
                if isinstance(obj, type):
                    return True
            # Fallback to capitalization heuristic
            return func.id[0].isupper()
        
        # Case: module.ClassName() or instance.method()
        if isinstance(func, ast.Attribute):
            # If we can evaluate the base, we can check if it's a class
            try:
                # This is a bit risky but we only do it for attributes
                # and we already ran imports.
                pass 
            except:
                pass
            return func.attr[0].isupper()
            
        return False

    def _execute_node(self, node: ast.AST):
        """
        Compiles and executes a single AST node in the local environment.
        """
        wrapper = ast.Module(body=[node], type_ignores=[])
        code_obj = compile(wrapper, filename="<snippet>", mode="exec")
        exec(code_obj, self.execution_globals)
