import os
import sys
# Add the subfolders to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), './'))
sys.path.append(os.path.join(os.path.dirname(__file__), './llm'))
sys.path.append(os.path.join(os.path.dirname(__file__), './email'))
sys.path.append(os.path.join(os.path.dirname(__file__), './mysqldb'))

from mails import sendEmailGeneral
from libs import TaskCelery


import time
from celery.result import AsyncResult
from tasks import process_jobs_tasks
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

saved_paths = ["media/pdf_job/Consultant Data Power BI.pdf", "media/pdf_job/Consultant Data Qlik.pdf","media/pdf_job/ML Engineer.pdf"]

result=process_jobs_tasks.delay(saved_paths, "gemini","yiyuemej@yahoo.fr")
print("check id")
print(result.id)
print("check status.")
print(result.status)

