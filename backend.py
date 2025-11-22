import re
from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from my_agent.agent import root_agent
from product_loader import initialize_products
import json

APP_NAME = "agents"
session_service = InMemorySessionService()
runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize products on application startup."""
    initialize_products("data.json")
    yield
    # Shutdown logic (if needed) would go here


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")

    if not message:
        return JSONResponse(
            {"error": "Message is required"}, 
            status_code=400
        )

    user_id = "user"
    session_id = "session"

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
    
    reply = ""

    # running the agent
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=Content(role="user", parts=[Part(text=message)]),
    ):
        if event.is_final_response():
            for part in event.content.parts:
                if hasattr(part, "text"):
                    reply += part.text

    try:
        # First, try parsing the entire reply as JSON
        structured_data = json.loads(reply.strip())
        if isinstance(structured_data, dict) and "products" in structured_data:
            return JSONResponse({
                "reply": structured_data.get("explanation", ""),
                "products": structured_data.get("products", [])
            })
    except json.JSONDecodeError:
        return JSONResponse({
            "reply": reply,
            "products": []
        })