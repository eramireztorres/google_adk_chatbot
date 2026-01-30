
import os
import sys
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import asyncio
import gc

# Add the experiment directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from initial_program import RAGSystem

load_dotenv()

def run_repro_fast():
    # Only use one file to speed up ingestion
    DOCS_PATH = "/tmp/repro_docs"
    os.makedirs(DOCS_PATH, exist_ok=True)
    with open(os.path.join(DOCS_PATH, "test.md"), "w") as f:
        f.write("# Test Document\nThis is a test document for reproduction.")
    
    # Use a fresh isolation path for LanceDB
    if os.path.exists("/tmp/lancedb_agno_repro"):
        import shutil
        shutil.rmtree("/tmp/lancedb_agno_repro")

    print("--- 1. Initializing RAG System (Agno) ---")
    # We monkeypatch the isolation path if needed, but for now we trust the default /tmp
    rag = RAGSystem(DOCS_PATH)
    
    print("\n--- 2. Running 1 Query ---")
    q = "What is in the test document?"
    print(f"Sample: {q}")
    res = rag.query(q)
    print(f"Agent response length: {len(res.get('answer', ''))}")
    
    eval_data = [{
        "question": q,
        "context": "\n".join(res.get("contexts", [])),
        "contexts": res.get("contexts", []),
        "prediction": res.get("answer", ""),
        "det_score": 0.5
    }]

    print("\n--- 3. Invoking Evidently (The Crash Point) ---")
    try:
        from evidently import Dataset
        from evidently.descriptors import ContextRelevance, FaithfulnessLLMEval
        
        df = pd.DataFrame(eval_data)
        # Using the exact same name as in the failing evaluator
        LLM_CONFIG = {"provider": "openai", "model": "gpt-4.1-nano"}
        
        print("Initializing Descriptors...")
        faithfulness = FaithfulnessLLMEval("prediction", context="context", alias="Faithfulness", **LLM_CONFIG)
        relevance = ContextRelevance("question", "contexts", aggregation_method="mean", method="llm", method_params=LLM_CONFIG, alias="Relevance")

        print("Calling Dataset.from_pandas...")
        # CRITICAL: This is the exact line from the traceback
        dataset = Dataset.from_pandas(df, descriptors=[faithfulness, relevance])
        print("SUCCESS! Evidently Dataset created successfully.")
        
    except Exception as e:
        print(f"\nREPRODUCED ERROR FOUND:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_repro_fast()
