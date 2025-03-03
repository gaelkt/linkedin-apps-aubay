import logging
from celery_app import app
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'mysqldb'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'parsing'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'llm'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'email'))

from chunks import processSingleJob, processSingleApplication 
from helper import generate_random_id
from libs import Task
from datetime import datetime
from libs import setLLM
from dotenv import load_dotenv
import time

from mails import computeEmailApplication, computeEmailJob

load_dotenv()

@app.task
def processMultipleJobs(saved_path_jobs, recipient_email, llm_type):
    
    try:
        

      logging.info("")
      logging.info("")
      logging.info("Started function processMultipleJobs")

      # Initializing variables
      number_jobs = len(saved_path_jobs) # Total number of jobs received
      count = 0   # Number of jobs processed
      success = 0  # number of jobs successfully run
      failure = 0 # number of jobs which failed
      output_log = []
      c_reel = 0

      is_job_already_in_database = 0
      numbers_jobs_in_database = 0

      logging.info(f"There is = {number_jobs} jobs to process")

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

        #logging.info(f"Processing job  {count + 1} / {number_jobs}")
        logging.info(f"successfull process this stape {success} / {number_jobs}")
        
        logging.info(f"get basename of {job_pdf_path}")

        # Filename of job description
        filename = os.path.basename(job_pdf_path)
        
        logging.info(f"filename = {filename}")
        
        logging.info("enter try clause")

        try:
            logging.info("call processSingleApplication")
            job, is_job_already_in_database = processSingleJob(job_pdf_path, mytask, llm)
            logging.info(f"Job processed  {job.role} successfully")
            success += 1
            current_output_log = {"filename": filename, "status": "success", "description": "New"}
        except Exception as e:
            failure += 1
            current_output_log = {"filename": filename, "status": "failed", "description": e}
            continue

        finally:
            count += 1
            output_log.append(current_output_log)

            # We have an old job that has not been processed with LLM
            if is_job_already_in_database:
                numbers_jobs_in_database += 1
                current_output_log["description"] = "job already in the database"
                logging.info("")
                logging.info("Job already in the database")
            
            # We have a new job that has been processed with LLM
            # We add 30s to avoid quota from Gemini
            else:
                logging.info("--------------------------------------------")
                logging.info("Waiting for 30 seconds")
                logging.info("--------------------------------------------")
                # time.sleep(25)

            output_log.append(current_output_log)

                
      logging.info("")
      logging.info(f"Finish processing {count} files")

      logging.info("")
      logging.info("Sending email ...")


      logging.info(f"Number of jobs received = {number_jobs}")
      logging.info(f"Number of jobs processed = {count}")
      logging.info(f"Number of jobs processed successfully = {success}")
      logging.info(f"Number of jobs already in database = {numbers_jobs_in_database}")


      logging.info(f"Sending email at {recipient_email}")
      computeEmailJob(recipient_email=recipient_email, jobs_received=number_jobs, jobs_processed=count, jobs_success=success, output_log=output_log)

      logging.info(f"Sent email at {recipient_email}")
    except Exception as e:
        logging.error(e)
    
    
    return 0


@app.task
def processMultipleApplications(saved_path_applications, recipient_email: str, llm_type: str = os.environ['LLM_TYPE']):
    try:
        
      logging.info("")
      logging.info("")
      logging.info("Started function processMultipleApplications")

      # Initializing variables
      number_applications = len(saved_path_applications)
      count = 0 # Number of applications processed
      success = 0  # Number of applications processed successfully
      failure = 0 # Number of applications processed with an error
      error_list = [] # List of applications which failed
      c_reel = 0

      output_log = []

      number_new_applications = 0



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

     # We process applications one by one
      for msg_file_path in saved_path_applications:

       
          logging.info("")
          logging.info("")

          logging.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
          logging.info(f"Processing application {count + 1}/{number_applications}")
          logging.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")

          logging.info("")


          # Filename of candidate application
          filename = os.path.basename(msg_file_path)

          try:
              logging.info("call processSingleApplication")
              application = processSingleApplication(msg_file_path=msg_file_path, task=task, llm=llm)

              if application.roleId != None:
                success += 1
                current_output_log = {"filename": filename, "status": "success", "description": "New"}
              else:
                current_output_log = {"filename": filename, "status": "aborted", "description": f"{application.role} is not yet in the database yet. Please register it under the tab Process Jobs."}
                failure += 1
            
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

          # We have an old application, we don't wait for 30s
          if application.isApplicationOld:
              current_output_log["description"] = "Application already in the database"
              logging.info(f"Candidate {application.name} has already applied to {application.role} position.")

        # We have a new application. We will wait for 30s
          else:
              number_new_applications += 1
              if count < number_applications:
                # logging.info("--------------------------------------------")
                # logging.info(f"Waiting for 25 seconds to start application {count+1}/{number_applications}")
                # logging.info("--------------------------------------------")
                # time.sleep(25)
                logging.info("Moving next application")

          output_log.append(current_output_log)

        # Saving task
      new_message = "Finish" + '\n ' +  task.message
      task.message = new_message + '\n ' +  task.message
      task.save(status="finish", message=new_message)




      logging.info(f"Number of applications received = {number_applications}")
      logging.info(f"Number of applications processed = {count}")
      logging.info(f"Number of applications processed successfully = {success}")

      logging.info("")
      logging.info(f"Preparing to send email at {recipient_email}")
      logging.info("")

      if os.environ['SEND_EMAIL']=="YES":
        computeEmailApplication(recipient_email=recipient_email, applications_received=number_applications, applications_processed=count, application_success=success, output_log=output_log)
        logging.info(f"Sent email at {recipient_email}")
    
      else:
        logging.info("")
        logging.info("Sending email is disabled")
        logging.info(f"os.environ['SEND_EMAIL']={os.environ['SEND_EMAIL']}")
        logging.info("Voici les LOGS")
        logging.info(f"output_log={output_log}")
      
    except Exception as e:
        logging.info("")
        logging.error(f"Error in function processMultipleApplications. Error = {e}")

    return 0

