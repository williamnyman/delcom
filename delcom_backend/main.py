from fastapi import FastAPI
from pydantic import BaseModel
from ranker import ranker_main
from fastapi.middleware.cors import CORSMiddleware
import threading

# --------------------------------------------------------------------------------
# this is the main backend file that runs the FastAPI server and handles requests
# --------------------------------------------------------------------------------


app = FastAPI()

# define a global variable to hold progress and result that will be changed later
progress = {"value": 0}
last_result = {"data": None}

# bypass CORS for local development, will change when deployed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# define class for craving request which is comprised of address and craving from frontend
class CravingRequest(BaseModel):
    address: str
    craving: str

# define the endpoint for craving requests
@app.post("/api/craving")
def craving_endpoint(data: CravingRequest):
    # have nested functions to run two threads, one for the ranker and one for the progress
    def run_ranker():
        def progress_callback(value: int):
            progress["value"] = value
        result = ranker_main(data.craving, data.address, progress_callback)
        progress["value"] = 100
        last_result["data"] = result

    threading.Thread(target=run_ranker, daemon=True).start()
    return {"status": "Ranking started"}

# define endpoint to get progress
@app.get("/progress")
def get_progress():
    return {**progress, "done": progress["value"] >= 100}

# define endpoint to get last (as in most recent) result
@app.get("/result")
def get_result():
    return last_result

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render sets this automatically
    uvicorn.run("main:app", host="0.0.0.0", port=port)
