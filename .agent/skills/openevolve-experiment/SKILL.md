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
*   **Small Modifications** (e.g., tuning parameters, optimizing specific functions):
    *   Use `diff_based_evolution: true`.
    *   The LLM will emit diff blocks to edit parts of the code/text.
*   **Full Rewrites** (e.g., rewriting prompts, changing entire algorithms):
    *   Use `diff_based_evolution: false`.
    *   The LLM will rewrite the entire text/file.

## 2. Generate `initial_program.py` (or `initial_prompt.txt`)
Create a baseline implementation.
*   **For Code (Diff-based)**:
    *   Must be a valid Python file.
    *   **CRITICAL**: If `diff_based_evolution: false`, you MUST wrap the code to be evolved with `# EVOLVE-BLOCK-START` and `# EVOLVE-BLOCK-END` to define the rewrite target.
    *   Example (for `diff_based_evolution: false`):
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
    *   A dictionary containing at least `"combined_score"`.
    *   **Score Direction**: Higher is BETTER. Normalize your metrics so that the goal is maximization.
    *   Can include other metrics like `"accuracy"`, `"speed"`, `"cost"`, etc., for the MAP-Elites grid.
*   **Robustness**:
    *   Import the candidate program dynamically using `importlib`.
    *   Wrap execution in `try/except` blocks.
    *   Implement timeouts (use `concurrent.futures` or similar) to prevent infinite loops in bad candidates.
    *   If the candidate fails, return `{"combined_score": 0.0, "error": "..."}`.

## 4. Generate `config.yaml`
Define the evolution hyperparameters.
*   **Basic Config**:
    ```yaml
    max_iterations: 50
    diff_based_evolution: true  # or false
    max_code_length: 10000
    log_level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    ```
*   **LLM Config**:
    *   Use `gpt-4.1-mini` as the default model.
    ```yaml
    llm:
      api_base: "https://api.openai.com/v1"
      model: "gpt-4.1-mini"
      temperature: 0.7
    ```
*   **Prompt Config**:
    *   `system_message`: A detailed prompt describing the expert persona (e.g., "Expert Performance Engineer") and the optimization goal.
    *   `include_artifacts`: Set to `true` to allow the LLM to see errors/feedback from previous iterations.
*   **Database Config**:
    *   `feature_dimensions`: Choose 2-3 metric names returned by your evaluator (e.g., `["complexity", "speed"]`).
    *   `exploitation_ratio`: Set low (e.g., 0.2) to favor diversity.
    *   `population_size`: Typicall 50-100.
*   **Evaluator Config**:
    *   `timeout`: Max seconds per evaluation.
    *   `parallel_evaluations`: Number of parallel workers (e.g., 4).
    *   `max_tasks_per_child`: Restart workers occasionally to prevent memory leaks (e.g., 10).

## 5. Generate `validate_setup.py`
Create a script to verify the setup before running evolution.
*   **Purpose**: Test that `evaluator.py` can successfully evaluate `initial_program.py` (or the initial text).
*   **Requirements**:
    *   Import `evaluate` from `evaluator`.
    *   Run `evaluate()` on the initial program path.
    *   Print the result.
    *   Assert that the result contains `combined_score` and no errors.


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
            "combined_score": score,
            "duration": duration,
            "complexity": len(open(program_path).read())
        }
    except Exception as e:
        return {"combined_score": 0.0, "error": str(e)}
```

## Config Template
```yaml
max_iterations: 20
diff_based_evolution: true

llm:
  model: "gpt-4.1-mini"

prompt:
  system_message: "You are an expert optimizer. Improve the code to run faster."

database:
  feature_dimensions: ["complexity", "duration"]

evaluator:
  timeout: 5
```
