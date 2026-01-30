
import os
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

def check_thread_pool(stage: str):
    print(f"\n--- Checking Thread Pool State at stage: {stage} ---")
    print(f"sys.is_finalizing(): {sys.is_finalizing()}")
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(lambda: "OK")
            print(f"ThreadPoolExecutor.submit: {future.result()}")
    except RuntimeError as e:
        print(f"ThreadPoolExecutor.submit FAILED: {e}")
    
    try:
        loop = asyncio.new_event_loop()
        res = loop.run_until_complete(asyncio.to_thread(lambda: "OK"))
        print(f"asyncio.to_thread: {res}")
        loop.close()
    except RuntimeError as e:
        print(f"asyncio.to_thread FAILED: {e}")

def run_diagnosis():
    load_dotenv()
    check_thread_pool("START")

    print("\n--- 1. Initializing Agno (Exp 2 Style) ---")
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        
        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            instructions=["Respond with OK"],
        )
        print("Calling agent.run()...")
        agent.run("test")
        print("Agno agent.run completed.")
    except Exception as e:
        print(f"Agno failed: {e}")

    check_thread_pool("AFTER_AGNO")

    print("\n--- 2. Simulating Cache Clear ---")
    # This is what I added to evaluator.py
    gc_collect = True
    if gc_collect:
        import gc
        gc.collect()
    
    check_thread_pool("AFTER_CLEANUP")

if __name__ == "__main__":
    run_diagnosis()
