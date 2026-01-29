from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BCABuddy Backend",
    description="Backend API for BCABuddy – IGNOU BCA AI Study Assistant",
    version="0.1.0"
)

# Allow frontend to talk to backend (important later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict karenge
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

