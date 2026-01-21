---
name: openevolve-experiment
description: Set up an evolutionary optimization experiment using the openevolve framework. Generates `config.yaml`, `evaluator.py`, and `initial_program.py` based on a user's optimization problem.
---

# Goal
Generate the required configuration and code files (`config.yaml`, `evaluator.py`, `initial_program.py`) to run an OpenEvolve evolutionary optimization experiment.

# Usage
Use this skill when the user asks to "set up an openevolve experiment", "optimize code using evolution", or "create an evolutionary optimizer" for a specific task.

# Instructions

## 1. Analyze the Problem
Determine the nature of the optimization task:
*   **Code Optimization** (e.g., speeding up a function, improving an algorithm):
    *   Use `diff_based_evolution: true`.
    *   The LLM will edit parts of the code.
*   **Prompt/Text Optimization** (e.g., improving an LLM prompt):
    *   Use `diff_based_evolution: false`.
    *   The LLM will rewrite the entire text.

## 2. Generate `initial_program.py` (or `initial_prompt.txt`)
Create a baseline implementation.
*   **For Code (Diff-based)**:
    *   Must be a valid Python file.
    *   **CRITICAL**: You MUST wrap the code to be evolved with `# EVOLVE-BLOCK-START` and `# EVOLVE-BLOCK-END`.
    *   Example:
        ```python
        # EVOLVE-BLOCK-START
        def slow_function(x):
            time.sleep(1)
            return x * 2
        # EVOLVE-BLOCK-END
        ```
*   **For Text/Prompts (Full rewrite)**:
    *   Just the raw text content to be optimized.

## 3. Generate `evaluator.py`
Create the scoring logic.
*   **Function Signature**: Must implement `evaluate(program_path) -> dict`.
    *   `program_path` is the absolute path to the candidate program file.
*   **Return Value**:
    *   A dictionary containing at least `"composite_score"` (or `"combined_score"`).
    *   **Score Direction**: Higher is BETTER. Normalize your metrics so that the goal is maximization.
    *   Can include other metrics like `"accuracy"`, `"speed"`, `"cost"`, etc., for the MAP-Elites grid.
*   **Robustness**:
    *   Import the candidate program dynamically using `importlib`.
    *   Wrap execution in `try/except` blocks.
    *   Implement timeouts (use `concurrent.futures` or similar) to prevent infinite loops in bad candidates.
    *   If the candidate fails, return `{"composite_score": 0.0, "error": "..."}`.

## 4. Generate `config.yaml`
Define the evolution hyperparameters.
*   **Basic Config**:
    ```yaml
    max_iterations: 50
    diff_based_evolution: true  # or false
    max_code_length: 10000
    ```
*   **LLM Config**:
    *   Use `gemini-2.5-flash` or `gemini-2.5-pro` as the default model.
    ```yaml
    llm:
      api_base: "https://generativelanguage.googleapis.com/v1beta/openai/"
      model: "gemini-2.5-flash"
      temperature: 0.7
    ```
*   **Prompt Config**:
    *   `system_message`: A detailed prompt describing the expert persona (e.g., "Expert Performance Engineer") and the optimization goal.
*   **Database Config**:
    *   `feature_dimensions`: Choose 2-3 metric names returned by your evaluator (e.g., `["complexity", "speed"]`).
    *   `population_size`: Typicall 50-100.
*   **Evaluator Config**:
    *   `timeout`: Max seconds per evaluation.
    *   `parallel_evaluations`: Number of parallel workers (e.g., 4).

# Example Output Structures

## Evaluator Template
```python
import importlib.util
import time

def evaluate(program_path):
    try:
        # Load candidate
        spec = importlib.util.spec_from_file_location("candidate", program_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test candidate
        start = time.time()
        result = module.solve_problem(test_input) # Assuming 'solve_problem' is the entry point
        duration = time.time() - start
        
        # Calculate Score (Higher is better)
        score = 1.0 / (1.0 + duration) 
        
        return {
            "composite_score": score,
            "duration": duration,
            "complexity": len(open(program_path).read())
        }
    except Exception as e:
        return {"composite_score": 0.0, "error": str(e)}
```

## Config Template
```yaml
max_iterations: 20
diff_based_evolution: true

llm:
  model: "gemini-2.5-flash"

prompt:
  system_message: "You are an expert optimizer. Improve the code to run faster."

database:
  feature_dimensions: ["complexity", "duration"]

evaluator:
  timeout: 5
```
