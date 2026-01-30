from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_engine import generate_reply
from rag_engine import RAGEngine
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup par RAG load hoga
try:
    rag_engine = RAGEngine()
except:
    rag_engine = None

class ChatPayload(BaseModel):
    message: str
    language: str
    mode: str  # Ye humara length_mode hai

@app.post("/chat")
async def chat_endpoint(payload: ChatPayload):
    try:
        # Context search
        context = rag_engine.search(payload.message) if rag_engine else ""
        
        reply = generate_reply(
            message=payload.message,
            context=context,
            language=payload.language,
            length_mode=payload.mode
        )
        return {"reply": reply}
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "Server error ho gaya hai!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)