import os
import json
import pandas as pd
import numpy as np
import importlib.util
import sys
import gc
from dotenv import load_dotenv
from openevolve.evaluation_result import EvaluationResult

# ==============================
# Evidently imports
# ==============================
try:
    from evidently import Dataset
    from evidently.descriptors import (
        ContextRelevance,
        FaithfulnessLLMEval,
    )
    EVIDENTLY_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Evidently imports failed: {e}")
    EVIDENTLY_AVAILABLE = False


def load_ground_truth(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File missing at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate(program_path):
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    
    # Verify API Key early to avoid silent failures
    if not os.getenv("OPENAI_API_KEY"):
        return EvaluationResult(
            metrics={"combined_score": 0.0},
            artifacts={"error": "OPENAI_API_KEY not found in environment or .env file"}
        )

    # ------------------------------
    # Paths and System Setup
    # ------------------------------
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAG_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
    
    # Add RAG root to path to allow importing adk_rag.utils
    if RAG_ROOT not in sys.path:
        sys.path.append(RAG_ROOT)
    
    try:
        from adk_rag.utils import PythonCodeExtractor, PythonSnippetChecker
    except ImportError:
        print("Warning: adk_rag.utils not found. Code checks will be skipped.")
        PythonCodeExtractor = None
        PythonSnippetChecker = None

    DOCS_PATH = os.path.join(RAG_ROOT, "docs", "adk_docs")
    GT_PATH = os.path.join(RAG_ROOT, "docs", "ground_truth", "adk_rag_evaluation_set.json")

    print(f"Debug: Evaluator running from: {SCRIPT_DIR}")
    print(f"Debug: Using ground truth at: {GT_PATH}")

    try:
        # ------------------------------
        # Load candidate program
        # ------------------------------
        print(f"--- Loading Candidate: {os.path.basename(program_path)} ---")
        spec = importlib.util.spec_from_file_location("candidate", program_path)
        candidate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(candidate)
        print("Debug: Candidate module loaded successfully.")

        if not hasattr(candidate, "evaluate_rag"):
            return EvaluationResult(
                metrics={"combined_score": 0.0},
                artifacts={"error": "Missing evaluate_rag function"}
            )

        # ------------------------------
        # Run inference and scoring
        # ------------------------------
        gt_data = load_ground_truth(GT_PATH)
        eval_data = [] # For Evidently
        sample_scores = [] # Overall combined per sample
        all_error_details = [] # Aggregated errors/details for the optimizer

        print(f"Running evaluation on {len(gt_data)} samples...")

        for idx, item in enumerate(gt_data):
            question = item.get("query")
            print(f"\n[Sample {idx+1}/{len(gt_data)}] Question: {question[:100]}...")
            mandatory_terms = item.get("mandatory_terms", [])
            penalized_terms = item.get("penalized_terms", [])
            requires_code = item.get("requires_code", False)

            try:
                result = candidate.evaluate_rag(DOCS_PATH, question)
                answer = result.get("answer", "")
                contexts = result.get("contexts", [])
                
                print(f"  - Answer received ({len(answer)} chars)")
                print(f"  - Retrieved {len(contexts)} contexts")
                
                # Context extraction helper (recursive)
                def _extract_text(c):
                    if isinstance(c, str): return c
                    if isinstance(c, dict): return str(c.get("page_content") or c.get("text") or c)
                    if hasattr(c, "page_content"): return str(c.page_content)
                    return str(c)

                context_list = [_extract_text(c) for c in (contexts if isinstance(contexts, list) else [contexts])]
                context_str = "\n".join(context_list)

                # --- 1. Deterministic Scoring ---
                det_score = 0.0
                logs = []
                
                # 1.1 Mandatory Terms
                terms_found = 0
                for term in mandatory_terms:
                    if term.lower() in answer.lower():
                        terms_found += 1
                    else:
                        logs.append(f"Missing mandatory term: {term}")
                if mandatory_terms:
                    det_score += (terms_found / len(mandatory_terms)) * 0.4 # Max 0.4
                
                # 1.2 Penalized Terms
                penalties = 0
                for term in penalized_terms:
                    if term.lower() in answer.lower():
                        penalties += 1
                        logs.append(f"Found penalized term: {term}")
                det_score -= (penalties * 0.1) # Penalty 0.1 per term
                
                # 1.3 Code Logic
                has_code = PythonCodeExtractor.has_python_code(answer) if PythonCodeExtractor else False
                if requires_code:
                    if has_code:
                        det_score += 0.2 # Reward for providing code
                    else:
                        det_score -= 0.3 # Penalty for missing code
                        logs.append("Missing required code snippet")
                elif has_code:
                    det_score += 0.1 # Bonus for helpful examples
                
                # 1.4 Code Quality
                if has_code and PythonCodeExtractor and PythonSnippetChecker:
                    code_snippet = PythonCodeExtractor.extract_robust(answer)
                    checker = PythonSnippetChecker(code_snippet)
                    check_res = checker.check()
                    if not check_res["success"]:
                        det_score -= 0.2
                        err_msg = check_res.get('error') or check_res.get('errors')
                        print(f"  - Code Error: {err_msg}")
                        logs.append(f"Code Quality Error: {err_msg}")
                        all_error_details.append({
                            "sample": idx, 
                            "type": "code_error", 
                            "message": str(err_msg),
                            "bad_code": code_snippet
                        })
                    else:
                        det_score += 0.1 # Bonus for valid code

                det_score = max(0.0, min(1.0, det_score)) # Clamp to [0, 1]
                print(f"  - Deterministic Score: {det_score:.2f} (Terms: {terms_found}/{len(mandatory_terms)})")

                # Store for Evidently
                eval_data.append({
                    "question": question,
                    "context": context_str,
                    "contexts": context_list,
                    "prediction": answer,
                    "det_score": det_score,
                    "logs": logs
                })

            except Exception as inf_err:
                print(f"Evaluation error for q='{question[:40]}...': {inf_err}")
                all_error_details.append({"sample": idx, "type": "inference_error", "message": str(inf_err)})
                eval_data.append({
                    "question": question, "context": "", "contexts": [], 
                    "prediction": "Error", "det_score": 0.0, "logs": [str(inf_err)]
                })

        # ------------------------------
        # LLM part via Evidently
        # ------------------------------
        if not EVIDENTLY_AVAILABLE or not eval_data:
            print("Warning: Skipping LLM evaluation (Evidently unavailable or no data).")
            combined_score = np.mean([d["det_score"] for d in eval_data]) if eval_data else 0.0
            return EvaluationResult(
                metrics={"combined_score": float(combined_score)},
                artifacts={"error": "Evidently not used", "num_samples": len(gt_data), "raw_scores": [d["det_score"] for d in eval_data]}
            )

        print(f"\nStarting LLM evaluation (Evidently) for {len(eval_data)} samples...")
        df = pd.DataFrame(eval_data)
        LLM_CONFIG = {"provider": "openai", "model": "gpt-4.1-nano"} # Standard for eval

        faithfulness = FaithfulnessLLMEval("prediction", context="context", alias="Faithfulness", **LLM_CONFIG)
        relevance = ContextRelevance("question", "contexts", aggregation_method="mean", method="llm", method_params=LLM_CONFIG, alias="Relevance")

        dataset = Dataset.from_pandas(df, descriptors=[faithfulness, relevance])
        res_df = dataset.as_dataframe()
        print("Debug: LLM evaluation complete.")

        # Final Combining
        final_scores = []
        for i, row in res_df.iterrows():
            # LLM part (0-1)
            # Map categorical labels if necessary
            label_map = {"FAITHFUL": 1.0, "PARTIALLY_FAITHFUL": 0.5, "UNFAITHFUL": 0.0}
            f_val = row.get("Faithfulness")
            if isinstance(f_val, str): f_val = label_map.get(f_val.upper(), 0.0)
            
            r_val = row.get("Relevance")
            if isinstance(r_val, list): r_val = np.mean(r_val) if r_val else 0.0
            
            llm_score = np.mean([f_val, r_val]) if not np.isnan(f_val) and not np.isnan(r_val) else f_val or r_val or 0.0
            
            # Weighted combine: 50% Deterministic, 50% LLM
            sample_combined = (row["det_score"] * 0.5) + (llm_score * 0.5)
            final_scores.append(sample_combined)

        combined_score = float(np.mean(final_scores)) if final_scores else 0.0
        print(f"Evaluation Complete. Combined Score: {combined_score:.4f}")
        
        metrics = {
            "combined_score": float(combined_score),
            "num_samples": len(gt_data),
        }
        artifacts = {
            "raw_scores": [float(s) for s in final_scores],
            "error_details": all_error_details
        }
        return EvaluationResult(metrics=metrics, artifacts=artifacts)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return EvaluationResult(
            metrics={"combined_score": 0.0},
            artifacts={"error": str(e), "traceback": traceback.format_exc()}
        )
    finally:
        # Crucial for stable multiprocessing cleanup
        print("Debug: Cleaning up memory (gc.collect)...")
        gc.collect()


if __name__ == "__main__":
    test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "initial_program.py")
    res = evaluate(test_path)
    print("Final Result:", res)
