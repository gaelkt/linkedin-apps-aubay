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


from utils import langchain_agent, langchain_agent_sql

from chunks import processJobs
from chunks import processMultipleApplications
from tasks import process_jobs_task, process_multiple_applications_task
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


import logging
import sys
import shutil
import time
from celery.result import AsyncResult
from tasks import process_job_task

# logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Jesus Christ is my Savior")




load_dotenv()
file_paths = []
openai.api_key = os.environ['OPENAI_API_KEY']

default_pdf_jobs_folder = os.environ['PDF_JOBS_FOLDER']
default_email_folder = os.environ['EMAIL_FOLDER']
default_resume_folder = os.environ['RESUME_FOLDER']

llm_type = os.environ['LLM_TYPE']


TEMP_FOLDER = os.environ['TEMP_JOB']
os.makedirs(TEMP_FOLDER, exist_ok=True)

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
@app.post("/job/")
async def multipleJob(files: List[UploadFile] = File(...), 
                       recipient_email: str = "gkamdemdeteyou@aubay.com",
                       llm_type: str = os.environ['LLM_TYPE']):


    # Checking validity of files
    validity=True
    invalid_files = []
    saved_paths=[]
    for file in files:
        if not file.filename.endswith(".pdf"):
            invalid_files.append(file)
            validity = False
            
        else:
            #file_path = os.path.join(TEMP_FOLDER, file.filename)
            file_path = f"media/pdf_job/{file.filename}"
            logging.info(f"Saving file {file_path}")
            with open(file_path, "wb") as f:
                f.write(await file.read())  # Sauvegarde le fichier
            saved_paths.append(file_path)  # Ajoute le chemin du fichier
            
            
    # At least one file is invalid
    if validity==False:
        logging.info(f"file {invalid_files} are not valid pdf files. Please choose files with format .pdf")
        content = {"message": f"files {invalid_files} are not valid pdf files. Please choose files with format .pdf"}
        return JSONResponse(content=content, status_code=400)
    
    # All job descs are valid
    # Function processJobs is run asynchronously
    logging.info("Processing jobs...")
    #await processJobs(files=files, recipient_email=recipient_email, llm_type = llm_type)
    
    
    
    logging.info("Sending task to Celery...")
    task = process_jobs_task.delay(saved_paths, recipient_email, os.environ['LLM_TYPE'])

    content = {"task_id": task.id,"message": f"Processing {len(files)} job descs"}

    return JSONResponse(content=content, status_code=200)

@app.post("/jobs/")
def multipleJobs(files: List[UploadFile] = File(...), 
                       recipient_email: str = "gkamdemdeteyou@aubay.com",
                       llm_type: str = os.environ['LLM_TYPE'], user: str=os.environ['USER']):
    
    # Checking validity of files
    validity = True
    invalid_files = []
    saved_paths = []
    for file in files:
        if not file.filename.endswith(".pdf"):
            invalid_files.append(file.filename)
            validity = False
        else:
            file_path = f"media/pdf_job/{file.filename}"
            logging.info(f"Saving file {file_path}")
            with open(file_path, "wb") as f:
                f.write(file.file.read())  # Sauvegarde le fichier
            saved_paths.append(file_path)  # Ajoute le chemin du fichier
    
    # At least one file is invalid
    if not validity:
        logging.info(f"Files {invalid_files} are not valid PDF files. Please choose files with format .pdf")
        content = {"message": f"Files {invalid_files} are not valid PDF files. Please choose files with format .pdf"}
        return JSONResponse(content=content, status_code=400)
    
    # All job descs are valid
    logging.info("Processing jobs...")
    
    tasks = {}
    
    # Lancer les tâches et stocker leur ID
    for path in saved_paths:
        print(f"Processing {path}")
        result = process_job_task.delay(path, llm_type)
        tasks[result.id] = {"path": path, "status": "PENDING", "result": None}
    
    # Vérifier l'état des tâches jusqu'à ce qu'elles soient toutes terminées
    while any(task["status"] not in ["SUCCESS", "FAILURE"] for task in tasks.values()):
        for task_id in tasks.keys():
            result = AsyncResult(task_id)
            current_status = result.status

            if current_status != tasks[task_id]["status"]:
                print(f"Tâche {task_id} - Nouveau statut : {current_status}")
                tasks[task_id]["status"] = current_status

                if current_status == "SUCCESS":
                    tasks[task_id]["result"] = result.result  # Stocker le résultat si nécessaire
                elif current_status == "FAILURE":
                    tasks[task_id]["result"] = f"Échec : {result.result}"

        time.sleep(5)  # Attendre avant la prochaine vérification
    
    # Une fois toutes les tâches terminées, envoyer un seul e-mail avec le résumé des résultats
    subject = "Processing of your jobs is done"
    body = "you have processed the following jobs :\n\n"
    
    for task_id, task_info in tasks.items():
        body += f"- File : {task_info['path']}\n  Status : {task_info['status']}\n  Résultat : {task_info['result']}\n\n"
        job_name = task_info['path'].split("/")[-1]
        if task_info["status"] == "SUCCESS":
            message = f"Successful process job {job_name}"
        else:
            message = f"Failed process job {job_name}"
        task = TaskCelery(
            Id=task_id,
            user=user,
            task_type="processing_jobs",
            date=datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            status=task_info["status"],
            message=message
        )
        
        task.save()
    
    sendEmailGeneral(recipient_email=recipient_email, message=body, subject=subject)
    
    print("E-mail envoyé avec le résumé des tâches.")
    
    return JSONResponse(content={"message": "Jobs processing started successfully."}, status_code=200)


# Endpoint used to process multiple applications and store their qualifications in the database
# Applications files are sent via a POST request
@app.post("/applications/")
async def multipleApplications(files: List[UploadFile] = File(...), 
        recipient_email: str = "gkamdemdeteyou@aubay.com",
        llm_type: str = os.environ['LLM_TYPE']):

    # Checking validity of files
    validity=True
    invalid_files = []
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
    

    # Function to process all the files asynchronously
    
    task = process_multiple_applications_task.delay(files, recipient_email, os.environ['LLM_TYPE'])
    
    #await processMultipleApplications(files=files, recipient_email=recipient_email, llm_type=llm_type)
    content = {"task_id": task.id,"message": f"Processing {len(files)} applications"}

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