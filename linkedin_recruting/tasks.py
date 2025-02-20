import logging
from celery_app import app
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'mysqldb'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'parsing'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'llm'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'email'))

from chunks import processSingleJob, processSingleApplication 
from helper import generate_random_date, generate_random_id
from libs import Application, Job, Task
from datetime import datetime
from libs import setLLM
from dotenv import load_dotenv
import time

from mails import sendEmailGeneral, computeEmailApplication

load_dotenv()

logging.info("File tasks.py")

@app.task
def processMultipleJobs(saved_path_jobs, recipient_email, llm_type):

    logging.info("")
    logging.info("")
    logging.info("Started function processMultipleJobs")

    # Initializing variables
    N = len(saved_path_jobs)
    count = 0
    success = 0  # number of jobs successfully run
    failure = 0 # number of jobs which failed
    error_list = [] # list of jobs who failed

    logging.info(f"There is = {N} jobs to process")

    mytask = Task(Id=generate_random_id(), user=os.environ['USER'], task_type="processing_jobs", 
            date=datetime.now().strftime("%Y-%m-%d %H-%M-%S"), status="running", 
            message="Started processing a single job")

    # We set the LLM
    llm = setLLM(llm_type=llm_type)
    logging.info("")
    logging.info(f"Using {llm_type} as LLM")

    # We run job desc after job
    for job_pdf_path in saved_path_jobs:

        logging.info("")
        logging.info("")
        logging.info("")

        logging.info(f"Processing job  {count + 1} / {N}")

        try:
            job = processSingleJob(job_pdf_path, mytask, llm)
            success += 1
        except Exception as e:
            failure += 1
            filename = os.path.basename(job_pdf_path)
            error_list.append({"filename": filename, "error": e})
            continue

        finally:
            count += 1

    logging.info("")
    logging.info(f"Finish processing {count} files")

    logging.info("")
    logging.info("Sending email ...")

    # We send email to recipient
    subject = "Processing of new job descs"
    message = f"Processing of new jobs ended. Received = {N} Processed = {count} success={success} and failed={failure} logs = {error_list} "
    
    logging.info(f"recipient_email={recipient_email}")
    sendEmailGeneral(recipient_email=recipient_email, message=message, subject=subject)

    logging.info("")
    logging.info("Email sent !!")
    

    return 0


@app.task
def processMultipleApplications(saved_path_applications, recipient_email: str, llm_type: str = os.environ['LLM_TYPE']):

    logging.info("")
    logging.info("")
    logging.info("Started function processMultipleApplications")

    # Initializing variables
    number_applications = len(saved_path_applications)
    count = 0 # Number of applications processed
    success = 0  # Number of applications processed successfully
    failure = 0 # Number of applications processed with an error
    error_list = [] # List of applications which failed

    output_log = []

    is_application_already_in_database=0
    is_application_new_in_database = 0



    # Generating a new task
    task = Task(Id=generate_random_id(), user=os.environ['USER'], task_type="multiple applications", 
        date=datetime.now().strftime("%Y-%m-%d %H-%M-%S"), status="running", 
        message="Started processing multiple candidate applications")

    logging.info(f"TaskId = {task.Id}")

    # We set the llm to use
    llm = setLLM(llm_type=llm_type)
    logging.info("")
    logging.info("")
    logging.info(f"Using {llm_type} as LLM")
    logging.info("")
    logging.info("")

   # We process applications one by one
    for msg_file_path in saved_path_applications:

       
        logging.info("")
        logging.info("")
        logging.info("")
        logging.info("")
        logging.info("")

        logging.info(f"Processing application {count + 1}/{number_applications}")
        logging.info("")
        logging.info("")
        logging.info("")

        filename = os.path.basename(msg_file_path)

        try:
            ApplicationData = processSingleApplication(msg_file_path=msg_file_path, task=task, llm=llm)
            success += 1
            current_output_log = {"filename": filename, "status": "success", "description": "Application processed successfully"}
            
        except Exception as e:
            failure += 1

            current_output_log = {"filename": filename, "status": "failed", "description": e}


            error_list.append({"filename": filename, "error": e})
            error_message = f"Error with file {filename}. Error={e}"
            logging.error(error_message)
            new_message = error_message + '\n ' +  task.message
            task.message = new_message + '\n ' +  task.message
            task.save(status="running", message=new_message)
            
            continue
        finally:
            count += 1

            # We wait one minute before continuing to avoid the quota limit of Gemini
            if count % 3 == 0:
                logging.info("")
                logging.info("")
                logging.info("")
                logging.info("")
                logging.info("--------------------------------------------")
                logging.info("Waiting for one minute")
                logging.info("--------------------------------------------")
                time.sleep(65)


        if ApplicationData==None:
            is_application_already_in_database += 1
            current_output_log["description"] = "Application already in the database"
        else:
            is_application_new_in_database += 1

        output_log.append(current_output_log)


    new_message = "Finish" + '\n ' +  task.message
    task.message = new_message + '\n ' +  task.message
    task.save(status="finish", message=new_message)




    logging.info(f"Sending email at {recipient_email}")
    logging.info(f"Number of applications received = {number_applications}")
    logging.info(f"Number of applications processed = {count}")
    computeEmailApplication(recipient_email=recipient_email, applications_received=number_applications,applications_processed=count, output_log=output_log)

    logging.info(f"Sent email at {recipient_email}")



    return 0

