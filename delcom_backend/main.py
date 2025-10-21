from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import threading
import os
import uvicorn
from ranker import ranker_main
import uuid

# ---------------------------------------------------------------------------
# FastAPI app setup
# ---------------------------------------------------------------------------

app = FastAPI()

# ✅ Store progress/results per session
sessions = {}

# ✅ Allowed frontend origins
origins = [
    "https://delcom.vercel.app",  # live frontend
    "http://localhost:5173",
    "https://delcom.vercel.app"      # local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------

class CravingRequest(BaseModel):
    address: str
    craving: str

# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.post("/api/craving")
def craving_endpoint(data: CravingRequest):
    """Start a background thread to process ranking for a new session."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"progress": 0, "result": None}

    def run_ranker():
        def progress_callback(value: int):
            sessions[session_id]["progress"] = value
        
        try:
            result = ranker_main(data.craving.strip(), data.address.strip(), progress_callback)
        except Exception as e:
            #print(f"Error in ranker_main: {e}")  # safe logging
            result = {"error": "Internal processing error"}
        sessions[session_id]["progress"] = 100
        sessions[session_id]["result"] = result

    threading.Thread(target=run_ranker, daemon=True).start()
    return {"status": "Ranking started", "session_id": session_id}

@app.get("/progress/{session_id}")
def get_progress(session_id: str):
    """Check current progress for a specific session."""
    session = sessions.get(session_id)
    if not session:
        return {"progress": 0, "done": False}
    return {"progress": session["progress"], "done": session["progress"] >= 100}

@app.get("/result/{session_id}")
def get_result(session_id: str):
    """Fetch the result for a specific session."""
    session = sessions.get(session_id)
    if not session:
        return {"data": None}
    return {"data": session["result"]}

# ---------------------------------------------------------------------------
# App entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
