
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

def test_conflict_theory():
    print("--- 1. Running Agno Agent ---")
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        
        # Initialize Agno Agent
        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            instructions=["Respond with 'OK'"],
        )
        
        # Running the agent. In Agno, 'run' is sync.
        # Theory: This calls asyncio.run() internally.
        print("Calling agent.run()...")
        response = agent.run("Hello")
        print(f"Agent response: {response.content}")
        
    except Exception as e:
        print(f"Agno failed: {e}")

    print("\n--- 2. Running evidently-style Async call ---")
    # Simulate evidently's async_to_sync behavior
    try:
        from openai import AsyncOpenAI
        
        async def mock_evidently_call():
            client = AsyncOpenAI()
            print("Attempting client.chat.completions.create...")
            # This triggers the platform check that uses asyncio.to_thread
            res = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            print("Call successful.")

        print("Creating new loop (like evidently does)...")
        new_loop = asyncio.new_event_loop()
        new_loop.run_until_complete(mock_evidently_call())
        
    except Exception as e:
        print(f"\nREPRODUCED ERROR:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_conflict_theory()
