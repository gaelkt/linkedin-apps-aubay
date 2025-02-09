import os
import sys
from docx2pdf import convert
# from pathlib import Path
from dotenv import load_dotenv
# from langchain_community.vectorstores import Chroma
# from langchain_community.vectorstores import Qdrant

# from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import PyMuPDFLoader

from PyPDF2 import PdfReader

from helper import generate_random_date
from datetime import datetime

from libs import setLLM

from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
import fitz

from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams




# Add the subfolders to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llm'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../mysqldb'))


from prompts import extractExperienceCandidat, extractDiplomeCandidat, extractHardSkillsCandidat, extractCertificationsCandidat
from prompts import extractExperienceRequired, extractDiplomeRequired, extractHardSkillsRequired, extractCertificationsRequired

import logging

from libs import Application, Job, Task

load_dotenv()
resume_folder = os.environ['RESUME_FOLDER']
llm_type = os.environ['LLM_TYPE']

# We create resume_folder if it does not exist
if not os.path.exists(resume_folder):
    os.makedirs(resume_folder)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def convert_word_2_pdf(word_path, pdf_path):
    
    try:
        
        if not os.path.isfile(word_path):
            logging.info(f"The word document does not exist {word_path}")
            raise Exception("Word document does not exists")
        convert(word_path, pdf_path)
        
    except Exception as e:
        logging.info(e)
        raise Exception(e)



def processSingleJob(job_pdf_path: str, task: str, llm) -> Job:

    if job_pdf_path == None:
        logging.info("Invalid input file. The can't be None")
        raise Exception("Invalid input file. The can't be None")

    elif not os.path.exists(job_pdf_path):
        logging.info(f"Invalid path. Can not find {job_pdf_path}")
        raise Exception(f"Invalid path. Can not find {job_pdf_path}")  

    job = Job(job_pdf_path=job_pdf_path, date=generate_random_date(), taskId=task.Id)

    logging.info(f"Job initalized with task = {job.taskId}")


    # Checking if the role is already in the database
    #If the role is already in the database we skip it

    if job.roleId == None:
        logging.info(f"...............=>Job {job.role} is not in the database yet. We generate roleId")
        job.roleId = setRoleId(job.role)

    else:
        logging.info(f"...............=>Job {job.role} is already in the database with roleID = {job.roleId}")
        return job

        
    # Extract chunk 
    job_desc_data= getChunk(job_pdf_path)[0].page_content
    logging.info(f"...............=>Job {job.role} resume data read")

    logging.info("")
    logging.info(f"...............=>Job {job.role} Extracting requirements")
    logging.info("")

    job.experience = extractExperienceRequired(context=job_desc_data, llm=llm)
    logging.info("")
    logging.info(f"...............=>Job {job.role} experience = {job.experience}")
    logging.info("")

    job.diplome = extractDiplomeRequired(context=job_desc_data, llm=llm)
    logging.info("")
    logging.info(f"...............=>Job {job.role} diplome = {job.diplome}")
    logging.info("")

    job.certifications =extractCertificationsRequired(context=job_desc_data, llm=llm)
    logging.info("")
    logging.info(f"...............=>Job {job.role} certifications = {job.certifications}")
    logging.info("")

    job.hard_skills = extractHardSkillsRequired(context=job_desc_data, llm=llm)
    logging.info("")
    logging.info(f"...............=>Job {job.role} Hard Skills = {job.hard_skills}")
    logging.info("")

    job.soft_skills = "NONE"
    job.langues = "NONE"

    # Saving job to mysql database
    logging.info(f"...............=>Saving job {job.role}")
    job.save()
    logging.info(f"...............=>Saved job {job.role}")

    return job

def processJobs(pdf_jobs_folder: str, task: Task):

    logging.info("Processing Job Description ....")


    '''
    Process a job desc and store requirements into a mysql database, and chunk in a vector database

    Input: 
        - pdf_jobs_folder: input folder for PDF job desc files 
        - embeddings: embeding for storage in a vector databse
        - vector_database: Vector database for storage of chunk

    Output: 
        - 0


    '''

    
    files = os.listdir(pdf_jobs_folder)
    
    logging.info(f"There are {len(files)} job desks")


    total_number_jobs = len(files)
    Failed = []

    failed_jobs = 0
    success_jobs = 0
    count = 0

    llm = setLLM(llm_type=llm_type)
    

    for i in range(len(files)):


        try:
            # ith job desk file
            logging.info("")
            logging.info("")
            logging.info("")
            file = pdf_jobs_folder + '/' + files[i]

            logging.info(f"job {count + 1}/{total_number_jobs}")

            job = processSingleJob(job_pdf_path=file, task=task, llm=llm)

            update_message = f"Success with {job.role}"
            logging.info(update_message)
            new_message = update_message + '\n ' +  task.message
            task.message = update_message + '\n ' +  task.message
            task.save(status="running", message=new_message)

            success_jobs += 1
            logging.info(f"...............=>Job {job.role} saved successfully in the database")
            count += 1
        
        except Exception as e:

            failed_jobs += 1
            Failed.append(files[i])

            error_message = f"Error when processing job {files[i]}. Error={e}"
            logging.error(error_message)

            new_message = error_message + '\n ' +  task.message
            task.message = new_message + '\n ' +  task.message
            task.save(status="running", message=new_message)

            count += 1
      
    final_message = "Task ended" + '\n ' + task.message
    task.message = final_message + '\n ' +  task.message
    task.save(status="success", message=final_message)
    logging.info("Finish with function processJobs")
    logging.info(f"Number of jobs = {total_number_jobs}  Success = {success_jobs}  Failed = {failed_jobs}")
    
    return total_number_jobs, success_jobs, failed_jobs, Failed

       
def getChunk(file_path):

    '''
    Generate single chunk from a pdf document

    Input: 
        - file_path: input PDF file 

    Output: 
        - chunks: 


    '''    
    
    # loader = PyPDFLoader(file_path)
    # documents = loader.load()

    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50000, chunk_overlap=0)  # Set high chunk size to avoid splitting

    chunks = text_splitter.split_documents(documents)

    if len(chunks) ==0 or len(documents)==0:

        logging.info(f"Issue when spliting file {file_path}. We have only {len(chunks)} chunks and {len(documents)} documents")

        raise Exception(f"Issue when spliting file {file_path}. We have only {len(chunks)} chunks and {len(documents)} documents")
        
    logging.info(f"Number of chunks={len(chunks)}")

    # Putting all content in one chunk
    if len(chunks) > 1:
        for i in range(1, len(chunks)):
            chunks[0].page_content = chunks[0].page_content + chunks[i].page_content

   
        
    # Deleting other chunks
    chunks = [chunks[0]]
    

    
    return chunks



def setRoleId(role):

    '''
        - This function is used to generate RoleID from Role name.
        - Later we will use random generation

    '''

    role_id = {"Tech Lead Data Engineering": "3kyBidhu",
            "Generative AI Engineer": "7hZ6glHq",
            "Consultant Data Power BI": "AIegN6My",
            "Consultant Teradata": "hcve6Ik8",
            "Consultant Data Management": "I0tLuRGw",
            "ML Engineer": "ieU9peuC",
            "Lead Power BI": "mIYDb0JL",
            "Data Engineer": "NBOqKK9H",
            "Consultant Data Qlick": "NJvt5YQB",
            "Consultant Data Qlik": "AS5fl5v0",
            "Consultant Data Integration – Informatica _ Talend": "pEumyRVP",
            "Consultant ETL IBM DataStage": "s4YIUtdV",
            "Data Solutions Architect": "KgY8qMd4"}


    return role_id[role]




def processApplication(msg_file_path, task, llm):


    '''
    Process a job application.

    Input: 
        - msg_file_path: msg file representing the CV of the candidate

    Output: 
        - applicationData: Json reprensenting the qualification of the candidate


    '''
    try:
        # Getting application metadata

        if not os.path.exists(msg_file_path):
            logging.error(f"File {msg_file_path} does not exist. Function processApplication")
            raise Exception(f"File {msg_file_path} does not exist")
        
        application = Application(msg_file_path)
        logging.info(f"Loaded application of {application.name} for {application.role} position")

        # We check if the candidate is already in the database
        if application.isApplicationOld:
            logging.info(f"{application.name} has already applied to {application.role} position.")
            return None


        # Extract chunk from pdf file
        #**********************************************************
        #**********************************************************
        #**********************************************************
        #                  Abdelaziz Jaddi va remplacer cette function

        chunk_resume = getChunk(application.pathResume)
        resume_data = chunk_resume[0].page_content
        logging.info("")
        logging.info(f"{len(chunk_resume)} chunks generated for name={application.name} role={application.role}.")
        logging.info("")

        # Saving data to vector store
        laparams = LAParams(line_overlap=0.5, detect_vertical=True, all_texts=True)
        text = extract_text(application.pathResume, laparams=laparams)

        if len(text) <=2:
            logging.info("")
            logging.info("")
            logging.info(f"Error in function processApplication. Unable to extract data from the resume of {application.name}. Check the pdf resume of the applicant")
            raise Exception(f"Error in function processApplication. Unable to extract data from the resume of {application.name}. Check the pdf resume of the applicant")

        second_chunk_resume=chunk_resume
        second_chunk_resume[0].page_content = text
        logging.info("Content filled with fitz")

        # Qdrant.from_documents(second_chunk_resume,
        #                       OpenAIEmbeddings(),
        #                       url=os.environ['qdrant_url'],
        #                       api_key = os.environ['qdrant_key'], 
        #                       collection_name = "fourted")
        logging.info("Data saved to vector store")


        application.diplome, application.annee_diplome, application.experience = extractExperienceCandidat(resume_data, llm=llm)
        logging.info(f"Candidate diplome={application.diplome} Candidate graduation={application.annee_diplome} Candidate experience={application.experience} .")

        # application.hard_skills = extractHardSkillsCandidat(resume_data, llm=llm)
        # logging.info(f"Candidate hard skills={application.hard_skills} .")
        application.hard_skills = "NONE"

        # application.certifications = extractCertificationsCandidat(resume_data, llm=llm)
        # logging.info(f"Candidate certifications={application.certifications} .")
        application.certifications = "NONE"

        # Loading job data
        logging.info("")
    
        # logging.info(f"Loading corresponding an empty job")
        job = Job(taskId=task.Id)
        roleId=application.roleId
        # logging.info(f"Loading corresponding job for roleId={roleId}")
        job.load(roleId=roleId)
        # logging.info(f"Loaded job role Id={job.roleId} Job experience={job.experience} Degree = {job.diplome}")

        # Calculatin application score
        application.scoring(job.experience, job.diplome)

        logging.info("")
        logging.info(f"Required exp={job.experience} Required Degree = {job.diplome}")
        logging.info(f"{application.score} score= {application.score} exp= {application.experience }  degree={application.diplome}")

        # Extract qualifications
        
        #**********************************************************
        #**********************************************************
        #**********************************************************
        #                  Abdelaziz Jaddi ICI
        #  def function_abdelaziz(context):
        #   - Input: contex[str]: Data of the resume
        #   - Output: experience[int]: experience
        #
        #   return experience
        #**********************************************************
        #**********************************************************
        # applicationData["experience"] = function_abdelaziz(context=chunks_application[0].page_content)

        # application.certifications = "None"
        # application.hard_skills = "None"
        application.soft_skills = "None"
        application.langues = "None"


        # Scoring
        # application.score = 100
        application.alternative_score = "None"
        application.alternative_role = "None"
        #**************************************************************
        #**************************************************************
        #**************************************************************
        application.save()
        logging.info(f"Saved application of {application.name} for role {application.role}.")


        return application

    except Exception as e:

        logging.error(f"Issue with job application {msg_file_path}. Error={e}")

        raise Exception(e)