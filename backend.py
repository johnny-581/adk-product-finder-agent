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
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

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

    class Product(BaseModel):
        id: int
        name: str
        description: str
        price: float
        image: str
        category: Optional[str] = None

    class AgentResponse(BaseModel):
        reply: str = Field(alias="reply", default="")
        products: List[Product] = Field(default_factory=list)

    # validation using pydantic
    try:
        cleaned_reply = reply.strip()
        if cleaned_reply.startswith("```json"):
            cleaned_reply = cleaned_reply[7:]
        elif cleaned_reply.startswith("```"):
            cleaned_reply = cleaned_reply[3:]
            
        if cleaned_reply.endswith("```"):
            cleaned_reply = cleaned_reply[:-3]

        response_data = AgentResponse.model_validate_json(cleaned_reply.strip())
        
        return JSONResponse({
            "reply": response_data.reply,
            "products": [p.model_dump() for p in response_data.products]
        })
    except (json.JSONDecodeError, ValidationError):
        # Fallback if the agent didn't return valid JSON
        return JSONResponse({
            "reply": reply,
            "products": []
        })