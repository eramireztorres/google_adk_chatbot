import os
import json
import pandas as pd
import numpy as np
import importlib.util
from dotenv import load_dotenv
from evidently import Dataset

# Try to import user requested metrics
try:
    from evidently import Report
    from evidently.presets import TextEvals
    from evidently.descriptors import (
        CorrectnessLLMEval,
        BERTScore,
        SemanticSimilarity,
        ContextRelevance,
        FaithfulnessLLMEval,
    )
    EVIDENTLY_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Evidently imports failed or signatures mismatch: {e}")
    # Fallback/Debug print to help user if specific import fails
    EVIDENTLY_AVAILABLE = False

def load_ground_truth(path):
    with open(path, 'r') as f:
        return json.load(f)

def evaluate(program_path):
    # Load environment
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    
    # Paths - using absolute paths as requested
    DOCS_PATH = "/home/erick/repo/google_adk_chatbot/rag/docs/adk_docs"
    GT_PATH = "/home/erick/repo/google_adk_chatbot/rag/docs/ground_truth/adk_docs_ground_truth_8.json"
    
    try:
        # 1. Import Candidate
        spec = importlib.util.spec_from_file_location("candidate", program_path)
        candidate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(candidate)
        
        if not hasattr(candidate, "evaluate_rag"):
            return {"combined_score": 0.0, "error": "Missing evaluate_rag function"}

        # 2. Run Inference
        gt_data = load_ground_truth(GT_PATH)
        eval_data = []
        
        print(f"Running inference on {len(gt_data)} samples...")
        
        for item in gt_data:
            question = item.get('input') or item.get('question')
            expected = item.get('expected_output') or item.get('answer')
            
            # Execute RAG
            try:
                result = candidate.evaluate_rag(DOCS_PATH, question)
                answer = result.get('answer', "")
                contexts = result.get('contexts', [])
                context_str = "\n".join(contexts) if isinstance(contexts, list) else str(contexts)
                
                # evidently expects: question, target, prediction, context
                eval_data.append([question, expected, context_str, answer])
            except Exception as inf_err:
                print(f"Inference error for q='{question[:20]}...': {inf_err}")
                eval_data.append([question, expected, "", "Error"])

        # 3. Compute Metrics with Evidently
        if not EVIDENTLY_AVAILABLE:
            return {"combined_score": 0.0, "error": "Evidently not installed"}

        # DataFrame columns must differ slightly for Evidently auto-mapping or manual mapping
        # We will use manual mapping in descriptors
        df = pd.DataFrame(eval_data, columns=['question', 'target', 'context', 'prediction'])
        
        print("Computing Evidently metrics...")
        
        # Define descriptors using signatures found in documentation
        # Note: We pass column names corresponding to our DataFrame
        
        print("Computing Evidently metrics...")
        
        # Define descriptors with aliases for easy extraction
        correctness = CorrectnessLLMEval(column_name="prediction", target_output="target", alias="Correctness")
        bert_score = BERTScore(columns=["prediction", "target"], alias="BERTScore")
        semantic_sim = SemanticSimilarity(columns=["prediction", "target"], alias="SemanticSimilarity")
        context_rel = ContextRelevance(input="question", contexts="context", alias="ContextRelevance")
        faithfulness = FaithfulnessLLMEval(column_name="prediction", context="context", alias="Faithfulness")
        
        descriptors_list = [correctness, bert_score, semantic_sim, context_rel, faithfulness]
        
        # Create Dataset with descriptors
        # This triggers computation when data is accessed
        dataset = Dataset.from_pandas(
            df,
            descriptors=descriptors_list
        )
        
        # Report visualization (optional but requested structure)
        report = Report(metrics=[TextEvals()])
        report.run(reference_data=None, current_data=dataset)
        
        # Extract scores directly from the computed dataset DataFrame
        # The dataframe will contain the original columns plus the descriptor aliases
        res_df = dataset.as_dataframe()
        
        scores = []
        for desc in descriptors_list:
            alias = desc.alias
            if alias in res_df.columns:
                # Take the mean of the column
                col_mean = res_df[alias].mean()
                if not np.isnan(col_mean):
                   scores.append(col_mean)
        
        if not scores:
            print("Warning: No scores found in resulting DataFrame.")
            combined_score = 0.0
        else:
            combined_score = np.mean(scores)
        
        print(f"Evaluation Complete. Combined Score: {combined_score:.4f}")
        
        return {
            "combined_score": float(combined_score),
            "num_samples": len(df),
            "raw_scores": scores
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"combined_score": 0.0, "error": str(e)}

if __name__ == "__main__":
    # Test run
    # Ensure initial_program.py exists in the same dir for this test
    test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "initial_program.py")
    res = evaluate(test_path)
    print("Final Result:", res)
