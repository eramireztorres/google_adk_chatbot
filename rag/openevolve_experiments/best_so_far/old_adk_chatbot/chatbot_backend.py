
import os
import json
import uuid
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from src.adk_chatbot.agents import create_agent_team
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
from src.adk_chatbot.auth import (
    init_auth_db,
    create_user,
    get_user_by_email,
    verify_password,
    create_access_token,
    decode_token,
)

# Define Request Model
class ChatRequest(BaseModel):
    message: str
    session_id: str

# Auth Models
class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# Initialize FastAPI
app = FastAPI(title="ADK Chatbot API")

# Global variables
agent_team: Agent = None
session_service = None
runner: Runner = None
APP_NAME = "adk_chatbot"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.on_event("startup")
async def startup_event():
    global agent_team, session_service, runner
    print("Initializing ADK Agent Team...")
    agent_team = create_agent_team()
    init_auth_db()
    db_url = os.getenv("ADK_SESSION_DB_URL", "sqlite:///./adk_sessions.db")
    session_service = DatabaseSessionService(db_url=db_url)
    
    # Initialize runner
    runner = Runner(
        agent=agent_team,
        app_name=APP_NAME,
        session_service=session_service
    )
    print("Agent Team Ready.")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    email = decode_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return email

@app.post("/auth/register")
async def register(request: RegisterRequest):
    existing = get_user_by_email(request.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    create_user(request.email, request.password)
    return {"status": "ok"}


@app.post("/auth/login")
async def login(request: LoginRequest):
    user = get_user_by_email(request.email)
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(request.email)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/auth/refresh")
async def refresh_token(user_email: str = Depends(get_current_user)):
    token = create_access_token(user_email)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/sessions")
async def create_session_endpoint(user_email: str = Depends(get_current_user)):
    session_id = str(uuid.uuid4())
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_email,
        session_id=session_id,
    )
    return {"session_id": session.id}


@app.get("/sessions")
async def list_sessions_endpoint(user_email: str = Depends(get_current_user)):
    resp = await session_service.list_sessions(app_name=APP_NAME, user_id=user_email)
    sessions = [
        {
            "id": s.id,
            "last_update_time": s.last_update_time,
            "state": s.state,
        }
        for s in resp.sessions
    ]
    return {"sessions": sessions}


@app.get("/sessions/{session_id}")
async def get_session_endpoint(session_id: str, user_email: str = Depends(get_current_user)):
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_email,
        session_id=session_id,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    events = []
    for ev in session.events:
        if hasattr(ev, "model_dump"):
            events.append(ev.model_dump())
        else:
            events.append(ev.__dict__)
    return {
        "id": session.id,
        "app_name": session.app_name,
        "user_id": session.user_id,
        "state": session.state,
        "events": events,
        "last_update_time": session.last_update_time,
    }

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, user_email: str = Depends(get_current_user)):
    global runner, session_service
    try:
        if not runner:
            raise HTTPException(status_code=500, detail="Runner not initialized")

        # RAG-only mode: bypass ADK agent routing and call MCP tool directly
        if os.getenv("RAG_ONLY_MODE") == "1":
            async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("get_adk_info", {"query": request.message})
                    payload = result.model_dump(by_alias=True, mode="json")
                    answer_text = ""
                    if payload.get("content"):
                        answer_text = payload["content"][0].get("text", "")
                    try:
                        parsed = json.loads(answer_text)
                        if isinstance(parsed, dict) and "answer" in parsed:
                            answer_text = parsed["answer"]
                    except Exception:
                        pass
                    return {"response": answer_text}

        # Ensure session exists (ADK requires session creation before run?)
        # Runner usually handles it, or we check existence. 
        # For simplicity, we assume create_session is idempotent or handle error.
        # Ensure session exists
        # Try creating; if it exists, ignore.
        try:
             await session_service.create_session(
                 app_name=APP_NAME,
                 user_id=user_email,
                 session_id=request.session_id,
             )
        except Exception as e:
             # Check if error message indicates existence (crude but effective for quick fix)
             if "already exists" not in str(e).lower():
                  pass # proceed, or log? safe to proceed usually if it's just 'exists'
        
        # Prepare content
        content = types.Content(role='user', parts=[types.Part(text=request.message)])
        
        # Run agent
        response_text = ""
        async for event in runner.run_async(
            user_id=user_email,
            session_id=request.session_id,
            new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    response_text = event.content.parts[0].text
                elif event.error_message:
                     response_text = f"Error: {event.error_message}"
        
        return {
            "response": response_text
        }
    except Exception as e:
        print(f"Error processing request: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
