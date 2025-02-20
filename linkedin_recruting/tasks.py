import logging
from celery_app import app
import sys
import os



sys.path.append(os.path.join(os.path.dirname(__file__), 'mysqldb'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'parsing'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'llm'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'email'))

from chunks import processSingleJob, processMultipleApplications # type: ignore
from mails import sendEmailGeneral
from libs import TaskCelery
from helper import generate_random_date, generate_random_id
from libs import Application, Job, Task
from datetime import datetime
from libs import setLLM
from dotenv import load_dotenv

load_dotenv()


@app.task
def process_job_task(job_pdf_path,llm_type):
    print("✅ process_job_task STARTED")
    
    task = Task(Id=generate_random_id(), user=os.environ['USER'], task_type="processing_jobs", 
            date=datetime.now().strftime("%Y-%m-%d %H-%M-%S"), status="running", 
            message="Started processing a single job")
    
    
    llm = setLLM(llm_type=llm_type)
    logging.info(f"Using {llm_type} as LLM")
    print(f"Into task.py : Using {llm_type} as LLM")

    logging.info(f"TaskId = {task.Id}")
    print(f"Into task.py :TaskId = {task.Id}")
    
    return processSingleJob(job_pdf_path, task, llm)
@app.task
def test_task(x, y):
    return x + y


@app.task
def simple_task(file_paths, recipient_email, llm_type):
    print("✅ process_jobs_task executed!")
    return f"Processing {len(file_paths)} files for {recipient_email}"




   
