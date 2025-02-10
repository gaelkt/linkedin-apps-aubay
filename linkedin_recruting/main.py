from dotenv import load_dotenv
import sys
import os
import openai 
from fastapi import FastAPI, Query
from fastapi import FastAPI, File, UploadFile
from typing import List
import uvicorn
from urllib.parse import unquote

from fastapi.responses import JSONResponse, FileResponse

from fastapi.middleware.cors import CORSMiddleware

# Add the subfolders to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'mysqldb'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'parsing'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'llm'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'email'))


from utils import langchain_agent, langchain_agent_sql

from chunks import processJobs, processSingleJob
from chunks import processApplication
from mysql_functions import refreshDB, getJobs
from mails import sendEmail, sendEmailGeneral
from libs import selectApplication, Task, setLLM
from datetime import datetime
from helper import generate_random_id

from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from typing import Optional

import logging
import sys


# logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Jesus Christ is my Savior")


#------------------

# logging = logging.getLogger("my_logging")
# logging.setLevel(logging.INFO)

# # Create handlers
# console_handler = logging.StreamHandler()  # Logs to the console
# file_handler = logging.FileHandler("app.log")  # Logs to a file

# # Set log levels for handlers
# console_handler.setLevel(logging.INFO)
# file_handler.setLevel(logging.ERROR)  # Only logs errors to the file

# # Create formatters
# console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# # Assign formatters to handlers
# console_handler.setFormatter(console_format)
# file_handler.setFormatter(file_format)

# # Add handlers to the logging
# logging.addHandler(console_handler)
# logging.addHandler(file_handler)

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

default_pdf_jobs_folder = os.environ['PDF_JOBS_FOLDER']
default_email_folder = os.environ['EMAIL_FOLDER']
default_resume_folder = os.environ['RESUME_FOLDER']

llm_type = os.environ['LLM_TYPE']

# We create resume_folder if it does not exist
if not os.path.exists(default_resume_folder):
    os.makedirs(default_resume_folder)

# We create email_folder if it does not exist
if not os.path.exists(default_email_folder):
    os.makedirs(default_email_folder)

# We create pdf job folder if it does not exist
if not os.path.exists(default_pdf_jobs_folder):
    os.makedirs(default_pdf_jobs_folder)


app = FastAPI(
    title="HR Server",
    version="1.0",
    description="A simple recruitment assistant API",
)

origins = [
    "http://localhost:5173", 
    "http://localhost:8081",
    "*"  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

add_routes(
    app,
    ChatOpenAI(model="gpt-3.5-turbo-0125"),
    path="/openai",
)

model = ChatOpenAI(model="gpt-3.5-turbo-0125")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
# add_routes(
#     app,
#     prompt | model,
#     path="/joke",
# )

# Endpoint used to setup the database and all tables
@app.get("/initialization/")
def initialize_database():

    logging.info("Initialzying the database ...")

     # We check database, then create database and all required table if they don't exist 
    refreshDB()

    content = {"message": f"Database {os.environ['DB_NAME']} is ready "}

    return JSONResponse(content=content, status_code=200)

# Endpoint used to view existing jobs in the database
# Return a Json where the key is the roleId of each job and the values a dict corresponding to the requirements of the job
@app.get("/view_jobs/")
def viewJobs():

    logging.info("Searching jobs the database ...")

    jobs = getJobs()

    return JSONResponse(content=jobs, status_code=200)

# Endpoint used to view existing applications in the database
# Return a Json where the key is the role of a job and the values a list of all candidates who applied to that job
@app.get("/view_applications/")
def viewApplications(begin_date, end_date, roles: list[str] = Query([])):

    selection = selectApplication(roles, begin_date, end_date)

    output = {}

    for role in selection:
        output[role] = [{"name": candidate.name, "score": candidate.score, "date":str(candidate.date),
        "experience":candidate.experience, "diplome":candidate.diplome, "annee_diplome":candidate.annee_diplome,
        "certifications":candidate.certifications, "hard_skills":candidate.hard_skills,
        "soft_skills":candidate.soft_skills, "langues":candidate.langues, "path":candidate.path} for candidate in selection[role]]


    return JSONResponse(content=output, status_code=200)

# Endpoint used to process multiple job and store its requirements in the database
# Jobs are sent via a POST request
@app.post("/jobs/")
async def multipleJobs(files: List[UploadFile] = File(...)):


    # Checking validity of files
    validity=True
    invalid_files = []
    for file in files:
        if not file.filename.endswith(".pdf"):
            invalid_files.append(file)
            validity = False
    if validity==False:
        logging.info(f"file {invalid_files} are not valid pdf files. Please choose files with format .pdf")
        content = {"message": f"files {invalid_files} are not valid pdf files. Please choose files with format .pdf"}
        return JSONResponse(content=content, status_code=400)

    # The files are valid
    logging.info("")
    logging.info("")

    # Counting application
    count = 0
    number_jobs = len(files)
    logging.info(f"There are {number_jobs} jobs")


    success, failed = 0, 0
    job_failed = []
    errors = []

    # We set the llm to use
    llm = setLLM(llm_type=llm_type)
    logging.info(f"Using {llm_type} as LLM")
    logging.info("")
    logging.info("")

    task = Task(Id=generate_random_id(), user=os.environ['USER'], task_type="processing_jobs", 
            date=datetime.now().strftime("%Y-%m-%d %H-%M-%S"), status="running", 
            message="Started processing a single job")

    logging.info(f"TaskId = {task.Id}")

   # We process applications one by one
  
    for file in files:
        try:
            input_pdf_file = f"media/pdf_job/{file.filename}"
            with open(input_pdf_file, "wb") as f:
                f.write(await file.read())


            count += 1

            logging.info("")
            logging.info("")
            logging.info("")

            logging.info(f"Processing application {count}/{number_jobs}")
            logging.info("")
            logging.info(f"input_pdf_file={input_pdf_file}")
            job = processSingleJob(input_pdf_file, task=task, llm=llm)

            # Updating task with success
            task.save(status="running", message=f"Job {job.role} has been successfully")
            success += 1

 
        except Exception as e:
            logging.info(f"We have an error with file. Error={file}")
            logging.info(f"The Error is {e}")
            job_failed.append(file)
            errors.append(e)
            failed += 1
 
    content = {"message": f"Processed {number_jobs} jobs",
                "number of success": success,
                "number of failed": failed,
                "jobs failed": job_failed,
                "errors": errors}
    return JSONResponse(content=content, status_code=200)





# Endpoint used to process multiple applications and store their qualifications in the database
# Applications files are sent via a POST request
@app.post("/applications/")
async def multipleApplications(files: List[UploadFile] = File(...)):

    # Checking validity of files
    validity=True
    invalid_files = []
    for file in files:
        if not file.filename.endswith(".msg"):
            invalid_files.append(file)
            validity = False
    if validity==False:
        logging.info(f"file {invalid_files} are not valid email message files. Please choose files with format .msg")
        content = {"message": f"files {invalid_files} are not valid email message files. Please choose files with format .msg"}
        return JSONResponse(content=content, status_code=400)

    # Files are valid email files

    # Number of applications
    number_applications = len(files)

    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"Processing {number_applications} applications ...")

    logging.info("")
    logging.info("")

    # Generating a new task
    task = Task(Id=generate_random_id(), user=os.environ['USER'], task_type="multiple applications", 
        date=datetime.now().strftime("%Y-%m-%d %H-%M-%S"), status="running", 
        message="Started processing multiple candidate applications")

    logging.info(f"TaskId = {task.Id}")


    count = 0
    is_application_already_in_database=0
    is_application_new_in_database = 0
    failed = 0
    failed_list = []

    # We set the llm to use
    llm = setLLM(llm_type=llm_type)
    logging.info(f"Using {llm_type} as LLM")
    logging.info("")
    logging.info("")

   # We process applications one by one
    for file in files:
        msg_file_path = f"media/temp/{file.filename}"
        with open(msg_file_path, "wb") as f:
            f.write(await file.read())


        count += 1

        logging.info("")
        logging.info("")
        logging.info("")
        logging.info("")
        logging.info("")

        logging.info(f"Processing application {count}/{number_applications}")
        logging.info("")

        # msg_file_path = email_folder + '/' + email_file

        try:
            ApplicationData = processApplication(msg_file_path=msg_file_path, task=task, llm=llm)
        except Exception as e:
            failed += 1
            error_message = f"Error with file {file}. Error={e}"
            logging.error(error_message)
            new_message = error_message + '\n ' +  task.message
            task.message = new_message + '\n ' +  task.message
            task.save(status="running", message=new_message)
            failed_list.append({"file": file, "error": str(e)})
            
            continue


        if ApplicationData==None:
            is_application_already_in_database += 1
        else:
            is_application_new_in_database += 1

    content = {"message": f"number of processed applications = {count}",
                "new applications": is_application_new_in_database,
                "applications in the database": is_application_already_in_database,
                "number applications failed": failed,
                "failed application list": failed_list
    }
    new_message = "Finish" + '\n ' +  task.message
    task.message = new_message + '\n ' +  task.message
    task.save(status="finish", message=new_message)

    email_message = "Finish processing applications"
    recipient_email = "gkamdemdeteyou@aubay.com"
    subject = "AI Recruiter assistant"
    sendEmailGeneral(recipient_email, email_message, subject)

    return JSONResponse(content=content, status_code=200)


@app.get("/report/")
def sendReport(recipient_email, begin_date, end_date, roles: list[str] = Query([])):

    # Selecting applications to send via email
    selection = selectApplication(roles, begin_date, end_date)

    # Sending selected applications
    sendEmail(recipient_email, selection, topN=10)
    
    logging.info("Finish !!!")
    content = {"message": "Report send"}

    return JSONResponse(content=content, status_code=200)

@app.get("/sql")
async def sql_selection(query: str):
    return langchain_agent_sql(query)
    

@app.get("/agent")
async def langchain_agent_core(query: str):
    return langchain_agent(query)
  
@app.get("/download/pdf_job/{filename}")
async def download_pdf_job(filename: str):
    filename = unquote(filename)
    file_path = os.path.join(default_pdf_jobs_folder, filename)
    
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")

    return FileResponse(file_path, filename=filename, media_type="application/pdf") # type: ignore

# Endpoint pour télécharger un fichier depuis resume
@app.get("/download/resume/{filename}")
async def download_resume(filename: str):
    filename = unquote(filename)
    file_path = os.path.join(default_resume_folder, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")

    return FileResponse(file_path, filename=filename, media_type="application/pdf")


if __name__ == "__main__":
    logging.info("Starting the server")

    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)