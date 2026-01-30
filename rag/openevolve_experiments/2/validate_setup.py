import sys
import os

def check_imports():
    print("Checking imports...")
    try:
        import agno
        from agno.agent import Agent
        from agno.knowledge.knowledge import Knowledge
        from agno.vectordb.lancedb import LanceDb
        print("✅ Agno imports successful.")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import check: {e}")
        return False

def check_env():
    print("\nChecking environment...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv("OPENAI_API_KEY"):
            print("✅ OPENAI_API_KEY found.")
        else:
            print("❌ OPENAI_API_KEY missing.")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Environment check failed: {e}")
        return False

if __name__ == "__main__":
    print(f"Python executable: {sys.executable}")
    imports_ok = check_imports()
    env_ok = check_env()
    
    if imports_ok and env_ok:
        print("\n🚀 Setup looks good for Agno Experiment!")
        sys.exit(0)
    else:
        print("\n⚠️  Setup has issues.")
        sys.exit(1)
