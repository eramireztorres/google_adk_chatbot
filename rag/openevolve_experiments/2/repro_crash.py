
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import asyncio

# Load environment
load_dotenv()

def test_repro():
    print("--- 1. Initializing Agno (Simulated) ---")
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        from agno.knowledge.knowledge import Knowledge
        from agno.vectordb.lancedb import LanceDb
        
        # We don't need real docs for this, just initialize the objects
        # as they would be in initial_program.py
        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            instructions=["Test"],
            search_knowledge=False
        )
        print("Agno Agent initialized.")
        # Trigger a dummy call to initialize openai client/threads
        # (We use run_test or similar if possible, but even init might be enough)
    except Exception as e:
        print(f"Agno init failed: {e}")

    print("\n--- 2. Initializing Evidently LLM Eval ---")
    try:
        from evidently import Dataset
        from evidently.descriptors import ContextRelevance, FaithfulnessLLMEval
        
        df = pd.DataFrame([{
            "question": "What is ADK?",
            "context": "ADK is a framework.",
            "contexts": ["ADK is a framework."],
            "prediction": "ADK is a framework.",
            "det_score": 1.0
        }])
        
        LLM_CONFIG = {"provider": "openai", "model": "gpt-4.1-nano"}
        
        faithfulness = FaithfulnessLLMEval("prediction", context="context", alias="Faithfulness", **LLM_CONFIG)
        relevance = ContextRelevance("question", "contexts", aggregation_method="mean", method="llm", method_params=LLM_CONFIG, alias="Relevance")

        print("Calling Dataset.from_pandas...")
        # This is where it crashes in the real evaluator
        dataset = Dataset.from_pandas(df, descriptors=[faithfulness, relevance])
        print("Evidently Dataset created successfully.")
        
    except Exception as e:
        print(f"\nCRITICAL ERROR FOUND:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_repro()
