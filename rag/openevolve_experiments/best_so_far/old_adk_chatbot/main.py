
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from google.genai import types
from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from google.adk.runners import Runner
from src.adk_chatbot.agents import create_agent_team

# Constants
APP_NAME = "adk_chatbot"
USER_ID = "local_user"
SESSION_ID = "cli_session_1"

async def main():
    print("Initializing AdK Chatbot Agent Team...")
    
    try:
        root_agent = create_agent_team()
    except Exception as e:
        print(f"Error creating agent team: {e}")
        return

    db_url = os.getenv("ADK_SESSION_DB_URL")
    if db_url:
        session_service = DatabaseSessionService(db_url=db_url)
    else:
        session_service = InMemorySessionService()
    
    # Create session
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    print("\n--- AdK Chatbot Ready ---")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except EOFError:
            break
            
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        
        if not user_input:
            continue
            
        print("Bot:", end=" ", flush=True)
        
        # Prepare the user's message in ADK format
        content = types.Content(role='user', parts=[types.Part(text=user_input)])
        
        try:
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=content
            ):
                # Simple streaming of final response or interesting events could go here
                # For now, we'll just wait for the final response
                if event.is_final_response():
                    if event.content and event.content.parts:
                        print(event.content.parts[0].text)
                    elif event.error_message:
                        print(f"[Error: {event.error_message}]")
        except Exception:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nUser interrupted.")
