import os
import json
import pandas as pd
import numpy as np
import importlib.util
from dotenv import load_dotenv

# ==============================
# Evidently imports (fixed)
# ==============================
try:
    from evidently import Dataset
    from evidently.presets import TextEvals
    from evidently.descriptors import (
        CorrectnessLLMEval,
        ContextQualityLLMEval,
        ContextRelevance,
        FaithfulnessLLMEval,
    )
    EVIDENTLY_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Evidently imports failed or signatures mismatch: {e}")
    EVIDENTLY_AVAILABLE = False


# ==============================
# Utils
# ==============================
def load_ground_truth(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File missing at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Mapping for categorical LLM outputs → numeric scores
LLM_LABEL_MAP = {
    "CORRECT": 1.0,
    "PARTIALLY_CORRECT": 0.5,
    "INCORRECT": 0.0,
    "FAITHFUL": 1.0,
    "PARTIALLY_FAITHFUL": 0.5,
    "UNFAITHFUL": 0.0,
    "GOOD": 1.0,
    "OK": 0.5,
    "BAD": 0.0,
}


def evaluate(program_path):
    # Load environment variables (.env with OPENAI_API_KEY)
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    # ------------------------------
    # Paths (robust)
    # ------------------------------
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAG_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

    DOCS_PATH = os.path.join(RAG_ROOT, "docs", "adk_docs")
    GT_PATH = os.path.join(RAG_ROOT, "docs", "ground_truth", "adk_docs_ground_truth_8.json")

    print(f"Debug: Evaluator running from: {SCRIPT_DIR}")
    print(f"Debug: Using docs at: {DOCS_PATH}")
    print(f"Debug: Using ground truth at: {GT_PATH}")

    try:
        # ------------------------------
        # Load candidate program
        # ------------------------------
        spec = importlib.util.spec_from_file_location("candidate", program_path)
        candidate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(candidate)

        if not hasattr(candidate, "evaluate_rag"):
            return {"combined_score": 0.0, "error": "Missing evaluate_rag function"}

        # ------------------------------
        # Run inference
        # ------------------------------
        gt_data = load_ground_truth(GT_PATH)
        eval_data = []

        print(f"Running inference on {len(gt_data)} samples...")

        for item in gt_data:
            question = item.get("input") or item.get("question")
            expected = item.get("expected_output") or item.get("answer")

            try:
                result = candidate.evaluate_rag(DOCS_PATH, question)
                answer = result.get("answer", "")
                contexts = result.get("contexts", [])
                def _extract_content(c):
                    # 1. If it's a string, just return it
                    if isinstance(c, str):
                        return c
                        
                    # 2. Try dictionary access (common in many frameworks)
                    if isinstance(c, dict):
                        for key in ["page_content", "text", "content", "body"]:
                            if key in c:
                                return str(c[key])
                        return str(c)  # Fallback: dump the dict
                        
                    # 3. Try attribute access (LangChain uses page_content, LlamaIndex uses text/get_content())
                    # LangChain
                    if hasattr(c, "page_content"):
                        return str(c.page_content)
                    # LlamaIndex (Node objects often have .text or .get_content())
                    if hasattr(c, "get_content") and callable(c.get_content):
                        return str(c.get_content())
                    if hasattr(c, "text"):
                        return str(c.text)
                        
                    # 4. Fallback
                    return str(c)

                if isinstance(contexts, list):
                    context_list = [_extract_content(item) for item in contexts]
                else:
                    context_list = [_extract_content(contexts)]
                
                context_str = "\n".join(context_list)

                eval_data.append([question, expected, context_str, context_list, answer])
            except Exception as inf_err:
                print(f"Inference error for q='{question[:40]}...': {inf_err}")
                eval_data.append([question, expected, "", [], "Error"])

        if not EVIDENTLY_AVAILABLE:
            return {"combined_score": 0.0, "error": "Evidently not installed"}

        df = pd.DataFrame(
            eval_data,
            columns=["question", "target", "context", "contexts", "prediction"],
        )

        print("Computing Evidently metrics...")

        # ------------------------------
        # LLM configuration (forced)
        # ------------------------------
        LLM_CONFIG = {"provider": "openai", "model": "gpt-4.1-nano"}

        # ------------------------------
        # Metrics
        # ------------------------------
        correctness = CorrectnessLLMEval(
            "prediction",
            target_output="target",
            alias="Correctness",
            **LLM_CONFIG,
        )

        faithfulness = FaithfulnessLLMEval(
            "prediction",
            context="context",
            alias="Faithfulness",
            **LLM_CONFIG,
        )

        context_quality = ContextQualityLLMEval(
            "context",
            question="question",
            alias="ContextQuality",
            **LLM_CONFIG,
        )

        context_relevance = ContextRelevance(
            "question",
            "contexts",
            output_scores=True,
            aggregation_method="mean",
            method="llm",
            method_params=LLM_CONFIG,
            alias="ContextRelevance",
        )

        descriptors_list = [
            correctness,
            faithfulness,
            context_quality,
            context_relevance,
        ]

        # ------------------------------
        # Dataset + computation
        # ------------------------------
        dataset = Dataset.from_pandas(df, descriptors=descriptors_list)

        # Optional report (not strictly required for scoring)
        report = TextEvals()
        # Not calling report.run() because Dataset already computed descriptors

        res_df = dataset.as_dataframe()

        # ------------------------------
        # Scoring (robust)
        # ------------------------------
        scores = []

        for desc in descriptors_list:
            alias = desc.alias
            if alias not in res_df.columns:
                continue

            col = res_df[alias]

            # Numeric metric
            if pd.api.types.is_numeric_dtype(col):
                val = col.mean()
                if not np.isnan(val):
                    scores.append(float(val))
            else:
                # List-based metric (e.g., per-context relevance scores)
                if col.apply(lambda v: isinstance(v, list)).any():
                    flat_vals = []
                    for item in col:
                        if isinstance(item, list) and item:
                            flat_vals.extend([v for v in item if isinstance(v, (int, float))])
                    if flat_vals:
                        scores.append(float(np.mean(flat_vals)))
                        continue

                # Categorical LLM metric
                mapped = col.astype(str).str.upper().map(LLM_LABEL_MAP)
                if mapped.notna().any():
                    scores.append(float(mapped.mean()))

        if scores:
            combined_score = float(np.mean(scores))
        else:
            combined_score = 0.0

        print(f"Evaluation Complete. Combined Score: {combined_score:.4f}")

        return {
            "combined_score": combined_score,
            "num_samples": len(df),
            "raw_scores": scores,
        }

    except Exception as e:
        import traceback

        traceback.print_exc()
        return {"combined_score": 0.0, "error": str(e)}


# ==============================
# Standalone test
# ==============================
if __name__ == "__main__":
    test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "initial_program.py")
    res = evaluate(test_path)
    print("Final Result:", res)
