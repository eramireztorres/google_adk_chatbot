import os
import json
import pandas as pd
import numpy as np
import importlib.util
import sys
import gc
from dotenv import load_dotenv

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
        return {"combined_score": 0.0, "error": "OPENAI_API_KEY not found in environment or .env file"}

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
            return {"combined_score": 0.0, "error": "Missing evaluate_rag function"}

        # ------------------------------
        # Run inference and scoring
        # ------------------------------
        gt_data = load_ground_truth(GT_PATH)
        all_scores = []
        all_code_errors = []
        all_error_details = []

        print(f"Running deterministic evaluation on {len(gt_data)} samples...")

        for idx, item in enumerate(gt_data):
            question = item.get("query")
            print(f"\n[Sample {idx+1}/{len(gt_data)}] Question: {question[:100]}...")
            mandatory_terms = item.get("mandatory_terms", [])
            penalized_terms = item.get("penalized_terms", [])
            requires_code = item.get("requires_code", False)

            try:
                result = candidate.evaluate_rag(DOCS_PATH, question)
                answer = result.get("answer", "")
                
                print(f"  - Answer received ({len(answer)} chars)")
                
                # --- Deterministic Scoring ---
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
                        all_code_errors.append(err_msg)
                        all_error_details.append({"sample": idx, "type": "code_error", "message": str(err_msg)})
                    else:
                        det_score += 0.1 # Bonus for valid code

                det_score = max(0.0, min(1.0, det_score)) # Clamp to [0, 1]
                print(f"  - Score: {det_score:.2f} (Terms: {terms_found}/{len(mandatory_terms)})")
                all_scores.append(det_score)

            except Exception as inf_err:
                print(f"Evaluation error for q='{question[:40]}...': {inf_err}")
                all_scores.append(0.0)
                all_error_details.append({"sample": idx, "type": "inference_error", "message": str(inf_err)})

        combined_score = float(np.mean(all_scores)) if all_scores else 0.0
        print(f"\nEvaluation Complete. Final Combined Score: {combined_score:.4f}")

        return {
            "combined_score": combined_score,
            "num_samples": len(gt_data),
            "raw_scores": all_scores,
            "code_errors": all_code_errors if all_code_errors else None,
            "error_details": all_error_details
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"combined_score": 0.0, "error": str(e)}
    finally:
        print("Debug: Cleaning up memory (gc.collect)...")
        gc.collect()

if __name__ == "__main__":
    test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "initial_program.py")
    res = evaluate(test_path)
    print("Final Result:", res)
