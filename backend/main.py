from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="BCABuddy Backend",
    description="Backend API for BCABuddy – IGNOU BCA AI Study Assistant",
    version="0.2.0"
)

# CORS (frontend connect ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict karenge
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Data Models (API Contract)
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
# Basic Routes
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


# -------------------------
# Chat Endpoint (Skeleton)
# -------------------------

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    """
    This is a placeholder chat endpoint.
    AI + RAG logic will be plugged in later.
    """

    dummy_reply = (
        "Abhi main warm-up mode me hoon 😄\n"
        "AI aur IGNOU content thodi der me add hoga.\n"
        "Par tension mat le — structure ready hai."
    )

    return ChatResponse(
        reply=dummy_reply,
        mode=payload.mode,
        language=payload.language
    )
