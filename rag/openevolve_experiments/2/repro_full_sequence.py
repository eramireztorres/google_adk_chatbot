
import os
import sys
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import asyncio
import gc

# Add the experiment directory to path to import RAGSystem
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from initial_program import RAGSystem

load_dotenv()

def run_repro():
    DOCS_PATH = "/home/erick/repo/google_adk_chatbot/rag/docs/adk_docs"
    
    print("--- 1. Initializing RAG System (Agno) ---")
    rag = RAGSystem(DOCS_PATH)
    
    print("\n--- 2. Running 10 Queries (Simulating Samples) ---")
    queries = [
        "What is Google ADK?",
        "How to create a tool?",
        "Explain tool context.",
        "What are agents?",
        "How to deploy?",
        "Explain memory.",
        "What is LanceDB?",
        "How to use OpenAI with Agno?",
        "Explain RAG.",
        "How to handle errors?"
    ]
    
    eval_data = []
    for i, q in enumerate(queries):
        print(f"Sample {i+1}/10: {q}")
        res = rag.query(q)
        eval_data.append({
            "question": q,
            "context": "\n".join(res.get("contexts", [])),
            "contexts": res.get("contexts", []),
            "prediction": res.get("answer", ""),
            "det_score": 0.5
        })

    print("\n--- 3. Invoking Evidently (The Crash Point) ---")
    try:
        from evidently import Dataset
        from evidently.descriptors import ContextRelevance, FaithfulnessLLMEval
        
        df = pd.DataFrame(eval_data)
        LLM_CONFIG = {"provider": "openai", "model": "gpt-4.1-nano"}
        
        faithfulness = FaithfulnessLLMEval("prediction", context="context", alias="Faithfulness", **LLM_CONFIG)
        relevance = ContextRelevance("question", "contexts", aggregation_method="mean", method="llm", method_params=LLM_CONFIG, alias="Relevance")

        print("Calling Dataset.from_pandas...")
        dataset = Dataset.from_pandas(df, descriptors=[faithfulness, relevance])
        print("Evidently Dataset created successfully!")
        
        # Optionally trigger actual LLM call to be sure
        # print("Accessing dataframe to trigger compute...")
        # print(dataset.as_dataframe().head())
        
    except Exception as e:
        print(f"\nREPRODUCED ERROR FOUND:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_repro()
