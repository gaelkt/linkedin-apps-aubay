from celery import Celery
from dotenv import load_dotenv
import os
load_dotenv()
import logging

# Configuration Celery
broker_host=os.environ.get("RABBITMQ_HOST")
broker_port=os.environ.get("RABBITMQ_PORT")
broker_user=os.environ.get("RABBITMQ_USER")
broker_password=os.environ.get("RABBITMQ_PASSWORD")

backend_host=os.environ.get("DB_HOST")
backend_user=os.environ.get("DB_USER")
backend_password=os.environ.get("DB_PASSWORD")
backend_db=os.environ.get("DB_NAME")

CELERY_BROKER_URL = 'pyamqp://aubay:aubay@localhost:5672//'
CELERY_RESULT_BACKEND = f"db+mysql+pymysql://{backend_user}:{backend_password}@{backend_host}/{backend_db}"

app = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.update(
    task_routes={
        "tasks.processMultipleJobs": {"queue": "aubay"},
        "tasks.processMultipleApplications": {"queue": "aubay"},
    },
    result_backend=CELERY_RESULT_BACKEND, 
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    worker_pool="solo",
)

logging.info(app.conf.broker_url)

import tasks  
app.autodiscover_tasks(["tasks"])
