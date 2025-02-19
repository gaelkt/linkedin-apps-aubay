from fastapi import FastAPI
from celery.result import AsyncResult
from celery_app import add,celery_app

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API FastAPI avec Celery et RabbitMQ"}

@app.post("/task/")
def run_task(x: int, y: int):
    task = add.delay(x, y)
    return {"task_id": task.id}

@app.get("/task/{task_id}")
def get_task_result(task_id: str):
    print(f"task_id: {task_id}")
    result = AsyncResult(task_id,app=celery_app)
    return {"task_id": task_id, "status": result.status, "result": result.result}
