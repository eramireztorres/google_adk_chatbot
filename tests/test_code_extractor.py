import pytest
from rag.adk_rag.utils import PythonCodeExtractor

def test_has_python_code():
    assert PythonCodeExtractor.has_python_code("Here is some code:\n```python\nprint('hello')\n```") is True
    assert PythonCodeExtractor.has_python_code("No code here.") is False
    assert PythonCodeExtractor.has_python_code("```py\nx=1\n```") is True
    assert PythonCodeExtractor.has_python_code("```\njust backticks\n```") is True
    assert PythonCodeExtractor.has_python_code("") is False

def test_extract_single_block():
    text = "Check this out:\n```python\ndef hello():\n    return 'world'\n```"
    expected = "def hello():\n    return 'world'"
    assert PythonCodeExtractor.extract(text) == expected

def test_extract_multiple_blocks():
    text = """
Step 1:
```python
x = 10
```
Step 2:
```py
print(x)
```
"""
    expected_list = ["x = 10", "print(x)"]
    expected_joined = "x = 10\n\nprint(x)"
    
    assert PythonCodeExtractor.extract(text, join=False) == expected_list
    assert PythonCodeExtractor.extract(text, join=True) == expected_joined

def test_extract_robust_heuristic():
    # If no backticks, but looks like code
    text = "import os\nprint(os.getcwd())"
    assert PythonCodeExtractor.extract_robust(text) == text.strip()

    # If backticks exist, use them
    text = "Here is code:\n```python\nx=1\n```\nAnd text."
    assert PythonCodeExtractor.extract_robust(text) == "x=1"

def test_extract_with_different_tags():
    text = "```PYTHON3\nprint('three')\n```"
    assert PythonCodeExtractor.extract(text) == "print('three')"

def test_empty_or_none():
    assert PythonCodeExtractor.extract("") == ""
    assert PythonCodeExtractor.extract("", join=False) == []
    assert PythonCodeExtractor.has_python_code(None) is False
