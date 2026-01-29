from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai_engine import generate_reply

app = FastAPI(
    title="BCABuddy Backend",
    description="Backend API for BCABuddy – IGNOU BCA AI Study Assistant",
    version="0.3.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Data Models
# -------------------------

class ChatRequest(BaseModel):
    message: str
    mode: str
    language: str = "hinglish"


class ChatResponse(BaseModel):
    reply: str
    mode: str
    language: str


# -------------------------
# Routes
# -------------------------

@app.get("/")
def root():
    return {
        "message": "BCABuddy backend is running 🚀",
        "status": "OK"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "BCABuddy backend"
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    reply = generate_reply(
        message=payload.message,
        mode=payload.mode,
        language=payload.language
    )

    return ChatResponse(
        reply=reply,
        mode=payload.mode,
        language=payload.language
    )
