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
*   **Complex Logic (e.g., RAG/Evidently)**:
    *   The `evaluate` function should import and call your complex evaluation logic (e.g., `from my_rag_eval import run_evaluation`).
    *   It MUST verify the result is a number and wrap it in the required dictionary format.
    *   Do NOT put all logic inside `evaluate` if it requires massive imports; keep it modular.

## 4. Generate `config.yaml`
Define the evolution hyperparameters.
*   **Basic Config**:
    ```yaml
    max_iterations: 50
    diff_based_evolution: true  # or false
    max_code_length: 10000
    max_code_length: 10000
    log_level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    ```
*   **LLM Config (STRICT)**:
    *   MUST be nested under `llm`.
    *   MUST include `model` and `api_base`.
    *   Do NOT use top-level `llm_model` or `parameters`.
    ```yaml
    llm:
      api_base: "https://api.openai.com/v1"
      model: "gpt-4.1-mini"
      temperature: 0.7
    ```
*   **Prompt Config (REQUIRED)**:
    *   MUST be nested under `prompt`.
    *   MUST include `system_message`.
    *   `include_artifacts`: `true` (highly recommended for error feedback).
    ```yaml
    prompt:
      system_message: "You are an expert optimizer..."
      include_artifacts: true
    ```
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

```python
import sys
import os
import importlib.util

def validate():
    print("Validating setup...")
    if not os.path.exists("evaluator.py"): sys.exit("evaluator.py missing")
    
    spec = importlib.util.spec_from_file_location("evaluator", "evaluator.py")
    eval = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(eval)
    
    try:
        res = eval.evaluate(os.path.abspath("initial_program.py"))
        print(f"Result: {res}")
        if isinstance(res, dict):
            score = res.get("combined_score")
        else: # EvaluationResult object
            score = res.metrics.get("combined_score")
            
        if score is None: raise ValueError("No combined_score in result")
        print("✅ Setup Valid")
    except Exception as e:
        print(f"❌ Validation Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate()
```


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
        
        # Prepare artifacts (optional but recommended)
        artifacts = {
            "execution_time": duration,
            "stdout": "Success"
        }

        # Return dict or EvaluationResult
        return {
            "combined_score": score, # CRITICAL: Must be present
            "duration": duration,
            "complexity": len(open(program_path).read()),
            "artifacts": artifacts
        }
    except Exception as e:
        import traceback
        return {
            "combined_score": 0.0, 
            "error": str(e),
            "artifacts": {"traceback": traceback.format_exc()}
        }
```

## Complex Evaluator Template (e.g. RAG)
```python
import importlib.util
# Import your specific evaluation logic helper 
# (assuming it exists or is generated alongside)
from my_rag_eval import run_evaluation_logic 

def evaluate(program_path):
    try:
        # 1. Load the candidate program (RAG pipeline)
        spec = importlib.util.spec_from_file_location("candidate", program_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 2. Run the complex evaluation
        # Pass the module or functions to your evaluator
        score, detailed_metrics = run_evaluation_logic(module)
        
        # 3. Return compatible result
        return {
            "combined_score": float(score),
            "metrics": detailed_metrics
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
