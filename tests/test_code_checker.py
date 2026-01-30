import pytest
from rag.adk_rag.utils import PythonSnippetChecker

def test_checker_valid_code():
    code = """
import os
import math
from datetime import datetime

# Instantiation
now = datetime.now()
"""
    checker = PythonSnippetChecker(code)
    result = checker.check()
    assert result["success"] is True

def test_checker_syntax_error():
    code = "import os\nif True"  # Missing colon
    checker = PythonSnippetChecker(code)
    result = checker.check()
    assert result["success"] is False
    assert result["stage"] == "parsing"
    assert "Syntax Error" in result["error"]

def test_checker_import_error():
    code = "import module_that_does_not_exist_xyz123"
    checker = PythonSnippetChecker(code)
    result = checker.check()
    assert result["success"] is False
    assert result["stage"] == "execution"
    assert any("Import Error" in e for e in result["errors"])

def test_checker_instantiation_error():
    code = """
from datetime import datetime
# This should fail if we try to instantiate with wrong args or something
# (Though our current heuristic only triggers on capitalized names)
obj = datetime("wrong args")
"""
    checker = PythonSnippetChecker(code)
    result = checker.check()
    assert result["success"] is False
    assert any("Instantiation Error" in e for e in result["errors"])

def test_checker_skips_long_running():
    # We want to ensure time.sleep(100) is NOT executed
    code = """
import time
import os
time.sleep(100)
"""
    import time
    start = time.time()
    checker = PythonSnippetChecker(code)
    result = checker.check()
    end = time.time()
    
    # If it ran time.sleep(100), it would take > 100s
    assert end - start < 1.0
    assert result["success"] is True

def test_checker_module_attribute_instantiation():
    code = """
import collections
dq = collections.Deque() # Note: Deque is capitalized in older versions or similar
"""
    # collections.deque is lowercase normally, but if a user writes collections.Counter()
    code2 = """
import collections
c = collections.Counter()
"""
    checker = PythonSnippetChecker(code2)
    result = checker.check()
    assert result["success"] is True
    assert "Counter" in str(checker.execution_globals["c"])
