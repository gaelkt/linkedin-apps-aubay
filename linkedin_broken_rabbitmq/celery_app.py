from celery import Celery # type: ignore

celery_app = Celery(
    'worker',
    broker='pyamqp://aubay:aubay@localhost:5672//',  # RabbitMQ broker URL
    backend="db+mysql+pymysql://root@localhost/celery_db" ,  # Using RPC as the result backend
    
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_backend="db+mysql+pymysql://root@localhost/celery_db", 
    worker_pool="solo",  
)
print(celery_app.conf.result_backend)
# Définition de la tâche
@celery_app.task
def add(x: int, y: int):
    return x + y
