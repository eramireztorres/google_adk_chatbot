import sys
import os
import importlib.util

def validate():
    print("Validating setup...")
    if not os.path.exists("evaluator.py"): 
        print("❌ evaluator.py missing")
        sys.exit(1)
    
    try:
        # Load evaluator module
        spec = importlib.util.spec_from_file_location("evaluator", "evaluator.py")
        eval_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(eval_mod)
        
        # Path to initial program
        prog_path = os.path.abspath("initial_program.py")
        if not os.path.exists(prog_path):
            print("❌ initial_program.py missing")
            sys.exit(1)
            
        print(f"Running evaluation on {prog_path}...")
        res = eval_mod.evaluate(prog_path)
        
        print(f"Result: {res}")
        
        if isinstance(res, dict):
            score = res.get("combined_score")
            error = res.get("error")
        else:
            print("❌ Result is not a dict")
            sys.exit(1)
            
        if error:
            print(f"❌ Evaluation returned error: {error}")
            sys.exit(1)
            
        if score is None: 
            print("❌ No combined_score in result")
            sys.exit(1)
            
        print(f"✅ Setup Valid. Score: {score}")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Validation Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate()
