from celery.result import AsyncResult
from tasks import multiple_task,test_task

# Test simple_task
print("we test the task")
tab=[4,6,11,25]
result=test_task.delay(4,6)
#result=multiple_task.delay(args=[tab])

print("we test the task")

print("check id")
print(result.id)
print("check status.")
print(result.status)
print("check result")
print(result.result)