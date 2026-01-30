from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Custom modules
from ai_engine import generate_reply
from rag_engine import RAGEngine

app = FastAPI(title="BCABuddy API")

# CORS fix for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
try:
    print("[STARTUP] RAG Engine loading...")
    rag_engine = RAGEngine()
    print("[STARTUP] RAG Engine ready! 🚀")
except Exception as e:
    print(f"[ERROR] RAG Engine load nahi hua: {e}")
    rag_engine = None

# Request Structure
class ChatPayload(BaseModel):
    message: str
    language: str
    mode: str  # This is our length_mode (Short/Medium/Long)

@app.get("/")
def health_check():
    return {"status": "running", "project": "BCABuddy"}

@app.post("/chat")
async def chat_endpoint(payload: ChatPayload):
    if not payload.message:
        raise HTTPException(status_code=400, detail="Empty message!")

    try:
        # Step 1: Search context from PDFs
        context = ""
        if rag_engine:
            context = rag_engine.search(payload.message)
        
        # Step 2: Generate AI reply
        reply = generate_reply(
            message=payload.message,
            context=context,
            language=payload.language,
            length_mode=payload.mode
        )

        return {"reply": reply}

    except Exception as e:
        print(f"[SERVER ERROR] {e}")
        return {"reply": "Server mein kuch gadbad hai. Please try again later."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)