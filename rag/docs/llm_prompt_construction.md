# OpenEvolve LLM Prompt Construction

This document explains what information OpenEvolve passes to the LLM during each evolution iteration.

## Overview

When `openevolve-run` executes, each iteration constructs a prompt containing:
1. System message
2. Current program's fitness and metrics
3. Evolution history (previous attempts, top programs, inspirations)
4. Artifacts from evaluation (errors, warnings, debug info)
5. The current program code
6. Task instructions

## Prompt Structure

The prompt is built by `PromptSampler.build_prompt()` at `openevolve/prompt/sampler.py:51-154`.

### System Message

A brief role definition from `openevolve/prompts/defaults/system_message.txt`:

```
You are an expert software developer tasked with iteratively improving a codebase.
Your goal is to maximize the FITNESS SCORE while exploring diverse solutions across feature dimensions.
The system maintains a collection of diverse programs - both high fitness AND diversity are valuable.
```

### User Message Template

From `openevolve/prompts/defaults/diff_user.txt`:

```markdown
# Current Program Information
- Fitness: {fitness_score}
- Feature coordinates: {feature_coords}
- Focus areas: {improvement_areas}

{artifacts}

# Program Evolution History
{evolution_history}

# Current Program
```{language}
{current_program}
```

# Task
Suggest improvements to the program that will improve its FITNESS SCORE.
...
```

## What Gets Included From the Evaluator

### Metrics Dictionary

**All values from the evaluator's `metrics` dictionary are passed to the LLM**, regardless of:
- Whether they are numeric or non-numeric (strings included)
- Whether they have a `_score` suffix or not

The formatting happens at `openevolve/prompt/sampler.py:156-168`:

```python
def _format_metrics(self, metrics: Dict[str, float]) -> str:
    formatted_parts = []
    for name, value in metrics.items():  # Iterates over ALL keys
        if isinstance(value, (int, float)):
            formatted_parts.append(f"- {name}: {value:.4f}")
        else:
            formatted_parts.append(f"- {name}: {value}")  # Strings included
    return "\n".join(formatted_parts)
```

### Special Handling for `combined_score`

The `combined_score` key has special treatment at `openevolve/utils/metrics_utils.py:88-93`:

```python
# Always prefer combined_score if available
if "combined_score" in metrics:
    return float(metrics["combined_score"])
```

This affects:
- The **Fitness Score** displayed at the top of the prompt
- Program ranking in the database
- Cascade evaluation thresholds

If `combined_score` is absent, fitness = average of all numeric metrics (excluding feature dimensions).

### Artifacts Dictionary

Artifacts are included if `include_artifacts: true` in config (default). They appear in a dedicated section showing execution output, errors, warnings, etc.

## Evaluator Return Formats

### Option 1: Plain Dict (Legacy)

```python
def evaluate(program_path):
    return {
        "combined_score": 0.85,
        "accuracy": 0.9,
        "debug_info": "some string"
    }
```

**Result:** The entire dictionary becomes metrics. ALL keys are shown to the LLM:

```
- combined_score: 0.8500
- accuracy: 0.9000
- debug_info: some string
```

**No automatic parsing** of nested `metrics` or `artifacts` keys from the root level.

### Option 2: EvaluationResult (Recommended)

```python
from openevolve.evaluation_result import EvaluationResult

def evaluate(program_path):
    return EvaluationResult(
        metrics={"combined_score": 0.85, "accuracy": 0.9},
        artifacts={"debug_info": "some string", "stderr": "warning..."}
    )
```

**Result:** Explicit separation of what the LLM sees:

| Section | Content |
|---------|---------|
| Metrics | `combined_score`, `accuracy` |
| Artifacts | `debug_info`, `stderr` |

## Evolution History Section

The prompt includes context from multiple programs:

### Previous Attempts (Last 3)

Shows recent evolution history with outcomes:

```
Attempt 5
- Changes: Modified cooling schedule
- Metrics: combined_score: 0.8500, accuracy: 0.9000
- Outcome: Improvement in all metrics
```

### Top Performing Programs (Default: 3)

Full code of the best programs from the current island:

```
Program 1 (Score: 0.9200)
```python
# Full program code here
```
Key features: Performs well on accuracy (0.9200)
```

### Diverse Programs (Default: 2)

Additional programs sampled for diversity, labeled D1, D2, etc.

### Inspiration Programs

Programs from different sources (migrants, random, high-performers) with type classification.

## Configuration Options

Key settings in `config.yaml` that affect prompt construction:

```yaml
prompt:
  num_top_programs: 3          # Programs shown in "Top Performing" section
  num_diverse_programs: 2      # Programs shown in "Diverse" section
  include_artifacts: true      # Whether to include execution artifacts
  max_artifact_bytes: 20480    # Max size per artifact (20KB default)
  use_template_stochasticity: true  # Randomize template wording
```

## Data Flow Summary

```
evaluate() returns dict or EvaluationResult
    ↓
_process_evaluation_result() → EvaluationResult
    ↓
metrics stored in database (Program.metrics)
artifacts stored in _pending_artifacts
    ↓
Next iteration samples parent program
    ↓
PromptSampler.build_prompt(
    current_program=parent.code,
    program_metrics=parent.metrics,      ← All metrics passed
    program_artifacts=parent_artifacts,  ← All artifacts passed
    previous_programs=...,
    top_programs=...,
    inspirations=...
)
    ↓
LLM receives formatted prompt with all information
```

## Example: Complete Prompt

Given an evaluator returning:

```python
return EvaluationResult(
    metrics={
        "combined_score": 0.85,
        "value_score": 0.78,
        "distance_score": 0.92
    },
    artifacts={
        "convergence_info": "Converged in 10 trials",
        "best_position": "x=-1.70, y=0.68"
    }
)
```

The LLM sees:

```markdown
# Current Program Information
- Fitness: 0.8500
- Feature coordinates: No feature coordinates
- Focus areas:
- Fitness improved: 0.7200 → 0.8500

## Last Execution Output

### convergence_info
```
Converged in 10 trials
```

### best_position
```
x=-1.70, y=0.68
```

# Program Evolution History

## Previous Attempts
Attempt 3
- Changes: Added momentum term
- Metrics: combined_score: 0.7200, value_score: 0.65, distance_score: 0.80
- Outcome: Mixed results

## Top Performing Programs
Program 1 (Score: 0.9100)
```python
def run_search():
    # Best performing code...
```
Key features: Performs well on combined_score (0.9100)

...

# Current Program
```python
def run_search():
    # Current parent code to be improved...
```

# Task
Suggest improvements to the program that will improve its FITNESS SCORE.
...
```

## Key Takeaways

1. **All metric keys are passed** to the LLM, not just numeric or `_score` suffixed ones
2. **Use `EvaluationResult`** to separate metrics from debugging artifacts
3. **`combined_score`** is special - used for fitness calculation and ranking
4. **Artifacts provide feedback** - errors and warnings guide the LLM's improvements
5. **Multiple programs shown** - top performers, diverse programs, and inspirations provide context
