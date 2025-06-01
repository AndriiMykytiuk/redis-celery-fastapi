from fastapi import FastAPI
from app.tasks import greet
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.post("/enqueue/")
def enqueue_task():
    task = greet.delay()
    return {"task_id": task.id, "status": "queued"}