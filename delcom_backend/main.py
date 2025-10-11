from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import threading
import os
import uvicorn
from ranker import ranker_main

# ------------------------------------------------------------------------------
# FastAPI app setup
# ------------------------------------------------------------------------------

app = FastAPI()

# Track background progress and result
progress = {"value": 0}
last_result = {"data": None}

# ✅ Define allowed frontend origins
origins = [
    "https://delcom.vercel.app",  # your live frontend
    "http://localhost:5173",      # local dev
]

# ✅ Configure CORS correctly
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Request model
# ------------------------------------------------------------------------------

class CravingRequest(BaseModel):
    address: str
    craving: str

# ------------------------------------------------------------------------------
# API routes
# ------------------------------------------------------------------------------

@app.post("/api/craving")
def craving_endpoint(data: CravingRequest):
    """Start a background thread to process ranking."""
    def run_ranker():
        def progress_callback(value: int):
            progress["value"] = value
        result = ranker_main(data.craving, data.address, progress_callback)
        progress["value"] = 100
        last_result["data"] = result

    threading.Thread(target=run_ranker, daemon=True).start()
    return {"status": "Ranking started"}

@app.get("/progress")
def get_progress():
    """Check current progress."""
    return {**progress, "done": progress["value"] >= 100}

@app.get("/result")
def get_result():
    """Fetch the most recent result."""
    return last_result

# ------------------------------------------------------------------------------
# App entry point (Render runs this)
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
