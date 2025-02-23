from dotenv import load_dotenv
import sys
import os
import openai 
from fastapi import FastAPI, Query, File, UploadFile
from typing import List
import uvicorn
from urllib.parse import unquote

from fastapi.responses import JSONResponse, FileResponse
from fastapi import HTTPException


from fastapi.middleware.cors import CORSMiddleware

# Add the subfolders to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'mysqldb'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'parsing'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'llm'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'email'))

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Jesus Christ is my Savior")

from utils import langchain_agent, langchain_agent_sql
#from chunks import processMultipleApplications
from tasks import processMultipleApplications, processMultipleJobs
#from tasks import process_jobs_task, process_multiple_applications_task
from mysql_functions import refreshDB, getJobs
from mails import sendEmail
from mails import sendEmailGeneral
from libs import TaskCelery
from libs import selectApplication, Task, setLLM
from datetime import datetime
from helper import generate_random_id

from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate



import sys
import shutil
import time
from celery.result import AsyncResult




logging.info("Finish")



openai.api_key = os.environ['OPENAI_API_KEY']

default_pdf_jobs_folder = os.environ['PDF_JOBS_FOLDER']
default_email_folder = os.environ['EMAIL_FOLDER']
default_resume_folder = os.environ['RESUME_FOLDER']
default_temp_folder = os.environ['TEMP_FOLDER']

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
# We create temp folder if it does not exist
if not os.path.exists(default_temp_folder):
    os.makedirs(default_temp_folder)


app = FastAPI(
    title="HR Server",
    version="1.0",
    description="A simple recruitment assistant API",
)

origins = [
    "http://localhost:5173", 
    "http://localhost:8081",
    "http://192.168.71.120:8081",
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Jesus Christ is my Savior")


# Endpoint used to setup the database and all tables
@app.get("/initialization/")
def initialize_database():

    logging.info("Initialzying the database ...")
    print("Initialzying the database ..")

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
        "experience":candidate.experience, "diplome":candidate.diplome, "freelance": "", "annee_diplome":candidate.annee_diplome,
        "certifications":candidate.certifications, "hard_skills":candidate.hard_skills,
        "soft_skills":candidate.soft_skills, "langues":candidate.langues, "path":candidate.path} for candidate in selection[role]]


    return JSONResponse(content=output, status_code=200)


@app.post("/jobs/")
def multipleJobs(files: List[UploadFile] = File(...), 
                       recipient_email: str = "gkamdemdeteyou@aubay.com",
                       llm_type: str = os.environ['LLM_TYPE'], user: str=os.environ['USER']):
    
    logging.info("multipleJobs...")
    # Checking validity of files
    validity = True
    invalid_files = []
    saved_path_jobs = []
    for file in files:
        if not file.filename.endswith(".pdf"):
            invalid_files.append(file.filename)
            validity = False

    # At least one file is invalid
    if not validity:
        logging.info(f"Files {invalid_files} are not valid PDF files. Please choose files with format .pdf")
        content = {"message": f"Files {invalid_files} are not valid PDF files. Please choose files with format .pdf"}
        return JSONResponse(content=content, status_code=400)
    
    # All job descs are valid and we save the path
    logging.info("Saving files for processing")

    for file in files:  
        file_path = f"media/pdf_job/{file.filename}"
        logging.info(f"Saving file {file_path}")
        with open(file_path, "wb") as f:
            f.write(file.file.read())  # Sauvegarde le fichier
        saved_path_jobs.append(file_path)  # Ajoute le chemin du fichier
    

    logging.info("All files saved. Now running asynchronous tasks...")
    print("All files saved. Now running asynchronous tasks...")
    output = processMultipleJobs.delay(saved_path_jobs, recipient_email, llm_type)
    logging.info("Finish with asynchronous tasks")
    logging.info(f"output={output}")
    celery_task_id = output.id
    logging.info(f"Task ID={celery_task_id}")
    result = AsyncResult(celery_task_id)
    logging.info(f"AsyncResult={result}")
    

    return JSONResponse(content={"message": f"Processing__ {saved_path_jobs} job descs. ID task: {celery_task_id}."}, status_code=200)
    


# Endpoint used to process multiple applications and store their qualifications in the database
# Applications files are sent via a POST request
@app.post("/applications/")
async def multipleApplications(files: List[UploadFile] = File(...), 
        recipient_email: str = "gkamdemdeteyou@aubay.com",
        llm_type: str = os.environ['LLM_TYPE']):

    # Checking validity of files
    validity=True
    invalid_files = []
    saved_path_applications = []

    for file in files:
        if not file.filename.endswith(".msg"):
            invalid_files.append(file)
            validity = False
            
    # At least one application is invalid
    if validity==False:
        logging.info(f"file {invalid_files} are not valid email message files. Please choose files with format .msg")
        content = {"message": f"files {invalid_files} are not valid email message files. Please choose files with format .msg"}
        return JSONResponse(content=content, status_code=400)

    # All the files are valid
    logging.info("Saving files for processing")
    
    for file in files:  
        file_path = f"media/temp/{file.filename}"
        logging.info(f"Saving file {file_path}")
        with open(file_path, "wb") as f:
            f.write(file.file.read())  # Sauvegarde le fichier
        saved_path_applications.append(file_path)  # Ajoute le chemin du fichier
    # Function to process all the files asynchronously
    
    output = processMultipleApplications.delay(saved_path_applications, recipient_email, os.environ['LLM_TYPE'])
    logging.info("Finish with asynchronous tasks")
    logging.info(f"output={output}")
    celery_task_id = output.id
    logging.info(f"Task ID={celery_task_id}")
    result = AsyncResult(celery_task_id)
    logging.info(f"AsyncResult={result}")

    return JSONResponse(content={"message": f"Processing {len(saved_path_applications)} applications. ID task: {celery_task_id}."}, status_code=200)





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
    logging.info("Example of logs")
    logging.info("This is a test")
    print("ok")
    logging.info("This is an info message")

    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
