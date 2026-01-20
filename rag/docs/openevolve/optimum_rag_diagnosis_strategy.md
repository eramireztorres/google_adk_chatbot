# Optimum RAG Diversity Diagnosis Strategy

This is a step-by-step playbook for an agent to determine why an OpenEvolve
RAG experiment is converging to small edits instead of architectural diversity.
All commands use the local virtualenv at `./venv`.

## 0) Environment Baseline

1. Confirm the virtualenv tools:
   - `./venv/bin/python -V`
   - `./venv/bin/pip -V`
2. If a required package is missing, install it in the venv:
   - `./venv/bin/pip install <package>`

## 1) Sanity Check The Baseline Program And Evaluator

1. Run the evaluator directly on the baseline program to ensure it passes:
   - `./venv/bin/python evaluator.py initial_program.py`
2. If it fails, fix the baseline first; OpenEvolve cannot evolve from a broken
   starting point.

## 2) Confirm What The LLM Is Allowed To Rewrite

1. Open `initial_program.py` and confirm the EVOLVE-BLOCK boundaries.
2. Check `config.yaml` for:
   - `diff_based_evolution` (set to `false` for major rewrites).
   - `allow_full_rewrites` (set to `true` if you want architecture changes).
3. If either is restrictive, plan a phase that enables full rewrites.

## 3) Verify Artifact Feedback Actually Reaches The LLM

1. Ensure `evaluator.enable_artifacts: true` is set.
2. Confirm the evaluator returns `EvaluationResult` with `artifacts` when an
   error occurs (or at least on failure cases).
3. Run a short evolution (5-10 iterations) and verify artifacts appear in
   `openevolve_output*/logs/` or candidate metadata.

## 4) Validate Feature Dimensions And Diversity Gates

1. If `database.feature_dimensions` includes `framework_id`, confirm the
   evaluator returns `framework_id` for every candidate (or remove the feature).
2. Ensure feature dimensions are raw values, not pre-binned.
3. If you use `cascade_evaluation`, check thresholds; too-high thresholds
   will discard diverse but initially weak candidates.

## 5) Instrument A Short "Exploration-First" Phase

1. Create a short phase (10-20 iterations) with:
   - `diff_based_evolution: false`
   - `allow_full_rewrites: true`
   - Higher `num_diverse_programs` than `num_top_programs`
   - `use_template_stochasticity: true`
2. Lower cascade thresholds or disable cascade to let risky candidates run.
3. Confirm at least one candidate switches frameworks or architecture.

## 5a) LlamaIndex-Only Diversity Phase (Recommended First)

1. Run a short LlamaIndex-only exploration to force internal diversity:
   - Use `config_llamaindex_diversity_phase.yaml`.
2. Target these specific LlamaIndex architectures:
   - `QueryEngineTool` + `SubQuestionQueryEngine`
   - `RouterQueryEngine` with `LLMSingleSelector`
   - Workflow-based RAG (`Workflow`, `step`, `StartEvent`, `StopEvent`)
3. Only after at least one of these candidates passes evaluation,
   expand to cross-framework exploration.

## 5b) Verify Framework Availability And Canonical Imports

1. Confirm the frameworks you list in the system message are installed:
   - `./venv/bin/python - <<'PY'`
     `import importlib;`
     `for m in ["llama_index.core","agno.agent","langchain_openai"]:`
     `    print(m, "OK" if importlib.util.find_spec(m) else "MISSING")`
     `PY`
2. If a framework is missing or its APIs differ, either:
   - Install the correct package versions in `./venv`, or
   - Remove that framework from the exploration phase system message.
3. Search for specific functions (e.g., `create_stuff_documents_chain`) to
   confirm they actually exist in your installed packages:
   - `rg -n "create_stuff_documents_chain" venv/lib/python3.13/site-packages`

## 6) Introduce External Knowledge When Needed

1. If models lack current framework knowledge, supply it explicitly:
   - Use optillm `readurls` to fetch docs, or
   - Embed curated snippets from `docs/adk_docs` into the system message.
2. Keep snippets short and actionable (imports, minimal examples, key classes).

## 7) Use Multi-Phase Evolution To Separate Architecture From Tuning

1. Phase 1 (exploration):
   - Focus on cross-framework architectures and tooling choices.
   - Accept lower scores; widen thresholds.
2. Phase 2 (exploitation):
   - Lock in the best framework and tune prompts/chunking/embeddings.
3. Preserve the best program from phase 1 as the seed for phase 2.

## 8) Test A Forced Architecture Jump

1. Create a temporary seed that is explicitly LangChain or Agno and run a
   short evolution to see if it stays in that framework.
2. If it still collapses to LlamaIndex, the issue is likely in the system
   message or strict evaluation constraints.

## 9) Inspect Failures And Classify Causes

1. For rejected candidates, classify by:
   - Import errors (missing packages, wrong imports)
   - API mismatch (framework signature changes)
   - Runtime errors (network or file access)
2. If errors are missing from artifacts, fix the evaluator to include them.
3. For repeated error patterns, add targeted guidance to the system message.

## 9b) When Import Errors Dominate

1. If logs show errors like:
   - `No module named 'langchain_core.chains'`
   - `cannot import name 'create_stuff_documents_chain'`
   then the allowed framework list does not match what is installed.
2. Resolve by either:
   - Installing the missing framework packages, or
   - Removing that framework from the system message for exploration.
3. Re-run a short exploration phase after the fix to confirm at least one
   non-LlamaIndex candidate executes successfully.

## 9c) When Loader/Reader Errors Dominate

1. If you see errors like `Error reading: <path>: 'str' object has no attribute 'seek'`,
   the Markdown reader is being called with a directory string instead of a file path.
2. Fix by forcing this ingestion pattern for Agno:
   - `reader = MarkdownReader()`
   - `for p in Path(docs_dir).rglob("*.md"): docs.extend(reader.read(p))`
3. If you see errors like `Error loading file .../adk-docs-agents-models.md` from LangChain,
   ensure `DirectoryLoader(..., loader_cls=TextLoader, silent_errors=True, recursive=True)`
   is used and avoid the default unstructured loader.
4. If you see LanceDb errors or empty contexts in Agno runs, ensure you are using
   `Knowledge(vector_db=LanceDb(...))` + `knowledge.load_documents(...)` and
   avoid `LanceDb.add_documents` or `LanceDb.index` (not part of the API here).

## 10) Check Evaluation Bias Against Diverse Architectures

1. If the evaluator expects a specific framework, relax those assumptions:
   - Avoid strict type checks against a single framework.
   - Accept multiple tool outputs or query engines.
2. If the evaluator enforces prompt format too tightly, broaden acceptance.

## 10b) Diagnose Embedding Failures Or Re-Embedding Per Query

1. Watch for repeated embedding calls per query (slow and costly) or
   zero/empty contexts (embedding failures).
2. Add a lightweight embedding health check to the RAG system:
   - Log when embeddings are created and how many vectors are stored.
   - Ensure embedding is done once per ingestion, not per query.
3. Validate that the index/vectorstore is cached across queries:
   - Use a singleton `RAGSystem` (already in boilerplate).
   - Ensure ingestion happens only in `__init__` or a one-time guard.
4. Test embedding output deterministically with a tiny probe:
   - Embed a fixed string once and confirm the vector length is non-zero.
5. If embeddings fail intermittently:
   - Check API rate limits and error logs in artifacts.
   - Reduce parallel evaluations to 1 (already set) and increase timeout.

## 10c) If Embedding API Connection Errors Stall The Run

1. If logs show repeated `APIConnectionError` or `Retrying request to /embeddings`,
   the run may never progress past the initial program.
2. Confirm the embedding provider is reachable and API key is valid.
3. Consider temporarily switching to a smaller or local embedding model if available.
4. Re-run a short 1-iteration test to confirm embeddings work before longer runs.

## 11) Run A Controlled Ablation Matrix

1. Short runs (10-20 iterations each) with only one variable changed:
   - `diff_based_evolution` on/off
   - With/without cascade evaluation
   - `num_diverse_programs` high vs low
   - With/without docs injection
2. Track changes in diversity (framework switches, architecture shifts).

## 12) Record Conclusions And Next Actions

1. Summarize which constraints or missing info caused convergence.
2. Keep a short list of required config changes for the next full run.
3. Store the best exploratory candidates as future seeds.

## Suggested Commands

Baseline evaluator:
```bash
./venv/bin/python evaluator.py initial_program.py
```

Short exploration run:
```bash
./venv/bin/openevolve-run initial_program.py evaluator.py --config config.yaml --iterations 10
```

Run with a specific seed:
```bash
./venv/bin/openevolve-run seed_langchain.py evaluator.py --config config.yaml --iterations 10
```
