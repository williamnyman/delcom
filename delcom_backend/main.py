from fastapi import FastAPI
from pydantic import BaseModel
from ranker import ranker_main
from fastapi.middleware.cors import CORSMiddleware
import threading

app = FastAPI()

progress = {"value": 0}
last_result = {"data": None}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CravingRequest(BaseModel):
    address: str
    craving: str

@app.post("/api/craving")
def craving_endpoint(data: CravingRequest):
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
    return {**progress, "done": progress["value"] >= 100}

@app.get("/result")
def get_result():
    return last_result
