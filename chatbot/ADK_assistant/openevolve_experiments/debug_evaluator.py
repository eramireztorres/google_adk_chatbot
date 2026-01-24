import sys
import os
import importlib.util
import time

# Paths
BASE_DIR = "/home/erick/repo/google_adk_chatbot/chatbot/ADK_assistant/openevolve_experiments"
INITIAL_PROGRAM = os.path.join(BASE_DIR, "initial_program.py")
EVALUATOR = os.path.join(BASE_DIR, "evaluator.py")

def main():
    print(f"Testing evaluation of {INITIAL_PROGRAM}")
    print(f"Using evaluator: {EVALUATOR}")
    
    # 1. Load evaluator module
    try:
        spec = importlib.util.spec_from_file_location("evaluator", EVALUATOR)
        eval_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(eval_module)
        print("✔ Evaluator module loaded successfully.")
    except Exception as e:
        print(f"❌ Failed to load evaluator: {e}")
        sys.exit(1)
    
    # 2. Run evaluate
    try:
        print("Starting evaluation (calling evaluate())...")
        start_time = time.time()
        result = eval_module.evaluate(INITIAL_PROGRAM)
        duration = time.time() - start_time
        
        print("\n" + "="*40)
        print(f"Evaluation completed in {duration:.2f}s")
        print("="*40)
        print(f"Result Type: {type(result)}")
        print(f"Result Content: {result}")
        print("="*40)
        
        if isinstance(result, dict) and result.get("combined_score") is not None:
             print("✔ Evaluation successful! Score obtained.")
        else:
             print("❌ Evaluation returned unexpected result structure or failure.")
             
    except Exception as e:
        print(f"❌ Evaluation failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
