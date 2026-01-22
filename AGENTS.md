# Repository Guidelines

## Project Structure & Module Organization
- `rag/` holds the main corpus for RAG experiments and docs.
- `rag/docs/` contains reference material, datasets, and example projects (Markdown and assets).
- `rag/openevolve_experiments/0/` contains runnable experiment scripts, configs, and outputs (for example `run_ingestion.py`, `config.yaml`).
- `requirements.txt` defines Python dependencies; `prompt_commands.txt` lists prompt helpers.
- `venv/` is a local virtual environment; treat it as machine-local, not source.

## Build, Test, and Development Commands
- Create and activate a virtualenv:
  - `python -m venv venv`
  - `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run an ingestion experiment: `python rag/openevolve_experiments/0/run_ingestion.py`
- Validate a setup: `python rag/openevolve_experiments/0/validate_setup.py`
- There is no centralized build step; most work is running scripts in `rag/`.

## Coding Style & Naming Conventions
- Python code should follow PEP 8 with 4-space indentation.
- Prefer descriptive, verb-based script names like `run_ingestion.py` or `validate_setup.py`.
- Keep configuration in `*.yaml` files near the scripts that use them.

## Testing Guidelines
- No repository-wide test runner is configured.
- Example tests live under `rag/docs/openevolve/examples/**/tests/` and are script-style.
- Run them directly, e.g. `python rag/docs/openevolve/examples/attention_optimization/tests/test_evaluator.py`.

## Commit & Pull Request Guidelines
- Existing commit messages are short, past-tense sentences (e.g., "Added ground-truth json"). Follow that style.
- PRs should include a brief summary, the motivation, and any dataset changes or new artifacts generated.

## Security & Configuration Tips
- Many dependencies expect API keys (OpenAI, Google, Pinecone). Use environment variables and avoid committing secrets.
- If you add configuration files with credentials, add them to `.gitignore` and document the required env vars.
