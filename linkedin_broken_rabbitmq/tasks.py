from linkedin_broken_rabbitmq.celery_app import celery_app

@celery_app.task
def add(x, y):
    return x + y
