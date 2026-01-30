
import os
import sys
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import gc

# Ensure we can import initial_program
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from initial_program import RAGSystem

# Mock Evidently Available
EVIDENTLY_AVAILABLE = True

def test_full_sequence_repro():
    load_dotenv()
    
    # 1. Setup Mock Docs
    DOCS_PATH = "/tmp/repro_docs_v2"
    os.makedirs(DOCS_PATH, exist_ok=True)
    for i in range(5):
        with open(os.path.join(DOCS_PATH, f"doc_{i}.md"), "w") as f:
            f.write(f"# Document {i}\nContent for document {i}. This mentions ADK.")

    print("--- 1. Initializing Agno RAG System (Exp 2 Style) ---")
    # This initializes LanceDB and background threads
    rag = RAGSystem(DOCS_PATH)

    print("\n--- 2. Running 10 Queries (Simulating Evaluator Loop) ---")
    eval_data = []
    for i in range(10):
        print(f"Sample {i+1}/10...")
        res = rag.query("What is ADK?")
        eval_data.append({
            "question": "What is ADK?",
            "context": "\n".join(res.get("contexts", [])),
            "contexts": res.get("contexts", []),
            "prediction": res.get("answer", ""),
            "det_score": 0.8
        })

    print("\n--- 3. Invoking Evidently (Expected Crash Point) ---")
    try:
        from evidently import Dataset
        from evidently.descriptors import ContextRelevance, FaithfulnessLLMEval
        
        df = pd.DataFrame(eval_data)
        LLM_CONFIG = {"provider": "openai", "model": "gpt-4.1-nano"}
        
        faithfulness = FaithfulnessLLMEval("prediction", context="context", alias="Faithfulness", **LLM_CONFIG)
        relevance = ContextRelevance("question", "contexts", aggregation_method="mean", method="llm", method_params=LLM_CONFIG, alias="Relevance")

        print("Calling Dataset.from_pandas...")
        dataset = Dataset.from_pandas(df, descriptors=[faithfulness, relevance])
        print("SUCCESS: No crash detected in sequence.")
        
    except Exception as e:
        print(f"\nREPRODUCED ERROR:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_sequence_repro()
