
import os
import sys
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import gc
import threading

# Ensure we can import initial_program
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from initial_program import RAGSystem

def test_cleanup_theory():
    load_dotenv()
    
    print("--- 1. Initializing Agno (Exp 2 Style) ---")
    rag = RAGSystem("/tmp/any_path") # Ingestion might fail but objects init
    
    print(f"Threads active after Agno init: {threading.active_count()}")
    for t in threading.enumerate():
        print(f"  - {t.name}")

    print("\n--- 2. Disposing Agno ---")
    del rag
    gc.collect() # Force cleanup
    
    print(f"Threads active after cleanup: {threading.active_count()}")

    print("\n--- 3. Invoking Evidently ---")
    try:
        from evidently import Dataset
        from evidently.descriptors import ContextRelevance, FaithfulnessLLMEval
        
        df = pd.DataFrame([{"question": "a", "context": "b", "contexts": ["b"], "prediction": "c"}])
        LLM_CONFIG = {"provider": "openai", "model": "gpt-4.1-nano"}
        
        dataset = Dataset.from_pandas(df, descriptors=[
            FaithfulnessLLMEval("prediction", context="context", alias="F", **LLM_CONFIG)
        ])
        print("SUCCESS: Evidently ran successfully after explicit cleanup.")
        
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cleanup_theory()
