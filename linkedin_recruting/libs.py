import os
import logging
from helper import generate_random_id, generate_random_date, convert_to_date
from pathlib import Path
import extract_msg
from helper import extract_applicant_name_from_subjet, extract_role_name_from_subject
from mysql_functions import check_application_exists, generate_engine, getRoleId, getJobData
from docx2pdf import convert
import numpy as np
from mysql_functions import getApplication
from sqlalchemy import text
from sqlalchemy import create_engine, Table, MetaData, update
import re

from dotenv import load_dotenv
load_dotenv()

resume_folder = os.environ['RESUME_FOLDER']


class TaskCelery:
    def __init__(self, Id, user, task_type, date, status="launched", message="The task is started"): 
        self.Id = Id
        self.user = user
        self.type = task_type
        self.date = date
        self.status = status
        self.message = message
        self.insert()
    def insert(self):
        engine = generate_engine()
        table_tasks = os.environ['CELERY_TABLE_TASKS']
        insert_query = f"""
        INSERT INTO {table_tasks} (Id, user, type, date, status, message)
        VALUES (:Id, :user, :type, :date, :status, :message);
        """
        values = {
        "Id": self.Id,
        "user": self.user,
        "type": self.type,
        "date": self.date,
        "status": self.status,
        "message": self.message
            }
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(text(insert_query), values)
                logging.info(f"...............=>Saved task {self.Id} to database")
        logging.info("Insertion ok")
        return 0
    def setId(self,id:str):
        self.Id=id
    def save(self, status="success", message="Task terminated"):
        logging.info(f"Saving task {self.Id} with status= {status} and message={message}")



class Task:
    
    def __init__(self, Id, user, task_type, date, status="launched", message="The task is started"): 

        self.Id = Id
        self.user = user
        self.type = task_type
        self.date = date
        self.status = status
        self.message = message

        self.insert()
 
    def insert(self):

        engine = generate_engine()
        table_tasks = os.environ['DB_TABLE_TASKS']


        insert_query = f"""
        INSERT INTO {table_tasks} (Id, user, type, date, status, message)
        VALUES (:Id, :user, :type, :date, :status, :message);
        """

        # Define the values to insert
        values = {
        "Id": self.Id,
        "user": self.user,
        "type": self.type,
        "date": self.date,
        "status": self.status,
        "message": self.message
            }


        # Execute the insertion
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(text(insert_query), values)
                logging.info(f"...............=>Saved task {self.Id} to database")
        
        logging.info("Insertion ok")
        return 0
    def setId(self,id:str):
        self.Id=id

    def save(self, status="success", message="Task terminated"):
        logging.info(f"Saving task {self.Id} with status= {status} and message={message}")
        
    def info(self, status="Pending", message="Task Pending"):
        
        logging.info(f"Saving task {self.Id} with status= {status} and message={message}")

        try:
            engine = generate_engine()
            # Connect to the database
            connection = engine.connect()
            table_tasks= os.environ['DB_TABLE_TASKS']
            metadata = MetaData()
            # Define metadata to reflect the table
            metadata = MetaData()
            tasks = Table(table_tasks, metadata, autoload_with=engine)

            # Update statement
            stmt = (update(tasks).where(tasks.c.Id == self.Id).values(status=status,message=message))

            # Execute the update
            result = connection.execute(stmt)

            # Commit the transaction
            connection.commit()
        
        except Exception as e:
            logging.info(f"Issue when updating task {self.Id}. Error={e}")




       
class Job:
    
    def __init__(self, taskId, job_pdf_path=None, date=None): 

        self.taskId = taskId

        self.path = job_pdf_path
    
        self.date = date
      
        if job_pdf_path != None:
            self.role = Path(job_pdf_path).stem
            self.roleId = getRoleId(self.role)
        else:
            self.role=None
            self.roleId = None
      
    
        self.experience = None

        self.diplome = None

        self.certifications = None

        self.hard_skills = None

        self.soft_skills = None

        self.langues = None
        

        
    def save(self):

        engine = generate_engine()
        table_name = os.environ['DB_TABLE_JOB']


        insert_query = f"""
        INSERT INTO {table_name} (roleId, role, date, path, experience, diplome, certifications, hard_skills, soft_skills, langues) 
        VALUES (:roleId, :role, :date, :path, :experience, :diplome, :certifications, :hard_skills, :soft_skills, :langues);
        """

        # Define the values to insert
        values = {
        "roleId": self.roleId,
        "role": self.role,
        "date": self.date,
        "path": self.path,
        "experience": self.experience,
        "diplome": self.diplome,
        "certifications": str(self.certifications),
        "hard_skills": str(self.hard_skills),
        "soft_skills": str(self.soft_skills),
        "langues": str(self.langues)
            }


        # Execute the insertion
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(text(insert_query), values)
                logging.info(f"...............=>Saved job {self.role} to database")
        

        return 0

    def load(self, roleId):

        if roleId == None:
            logging.info("roleId can not be None in Job.load(self, roleId)")
            raise Exception("roleId can not be None in Job.load(self, roleId)")

        _, job_data = getJobData(roleId)

        self.path = (job_data["path"]).replace("\\", "/")
    
        self.date = job_data["date"]
      
        self.role = job_data["role"]
      
        self.experience = job_data["experience"]

        self.diplome = job_data["diplome"]

        self.certifications = job_data["certifications"]

        self.hard_skills = job_data["hard_skills"]

        self.soft_skills = job_data["soft_skills"]

        self.langues = job_data["langues"]

        return self.role


class Application:
    def __init__(self, msg_file_path=None, Id=None, roleId=None, name=None,
    role=None, date=None, score=None, experience=None, diplome=None, annee_diplome=None,
    alternative_score=None, alternative_role=None, certifications=None,
    hard_skills=None, soft_skills=None, langues=None, path=None):

        if msg_file_path ==None:
            self.Id = Id
            self.roleId = roleId
            self.name = name
            self.role = role
            self.date = date
            self.score = score
            self.experience = experience
            self.diplome = diplome
            self.annee_diplome = annee_diplome
            self.alternative_score = alternative_score
            self.alternative_role = alternative_role
            self.certifications = certifications
            self.hard_skills = hard_skills
            self.soft_skills = soft_skills
            self.langues = langues
            self.path = path

            return None
        
        # We check if email file exists
        elif not os.path.exists(msg_file_path):
            logging.info(f"The following email file does not exists {msg_file_path}.")
            raise Exception(f"The following email file does not exists {msg_file_path}")


        # Load the .msg file
        try:
            msg = extract_msg.Message(Path(msg_file_path))
        except Exception as e:
            logging.error(f"Unable to open email file at {msg_file_path}.")
            raise Exception(f"Unable to open email file {msg_file_path}. Error={e}") 

        msg_subject = msg.subject if msg.subject else "No Subject"

        # Folder where the resume will be saved
        self.folder = resume_folder

        # Name of the applicant
        self.name = extract_applicant_name_from_subjet(msg_subject)
        
        # Date of the application
        if msg.date:
            self.date =convert_to_date(str(msg.date)) 
        
        else: 
            raise Exception(f"Unknown Date for Application {msg_file_path}")

        # Role of the application
        self.role = extract_role_name_from_subject(str(msg_subject))


        # ID of the role
        self.roleId = getRoleId(self.role)
        if self.roleId==None:

            # If we can not find the roleId in DB we try to extract the role name from email path and try one more time
            email_file =  Path(msg_file_path).stem
            role = extract_role_name_from_subject(str(email_file))
            roleId = getRoleId(role)

            if roleId == None:
                logging.info(f"Role {self.role} is not in the job database yet")
                raise Exception(f"Role {self.role} is not in the job database yet")
            else:
                self.role = role
                self.roleId = roleId
                logging.info(f"role={self.role} roleId={self.roleId}")


        # We generate a random ID for the application
        self.Id = generate_random_id()

        # We check if the application is new or not
        self.isApplicationOld = check_application_exists(self.name, self.role)

        self.attachementCount = len(msg.attachments)


        self.pathResume = self.getResume(msg)
        logging.info(f"Resume extracted and saved at {self.pathResume}")
        
        
        # Candidate qualifications
        self.experience = None
        
        self.diplome = None

        self.annee_diplome = None
        
        self.certifications = None
        
        self.hard_skills = None
        
        self.soft_skills = None
        
        self.score = 0

        logging.info(f"Application initialized for {self.name}")

    
    def getResume(self, msg):

        try:

            # Check for any attachments
            if msg.attachments:
                logging.info(f"There is {len(msg.attachments)} attachement(s)....")

                for attachment in msg.attachments:

                    if attachment.longFilename == None:
                        logging.error("attachement name is None")
                        raise Exception("attachement name is None")

                    attachment.save(customPath=self.folder, customFilename=attachment.longFilename)


                    attachement_file_path = os.path.join(self.folder, attachment.longFilename)

                    _, extension = os.path.splitext(attachment.longFilename)

            

                    if extension != ".pdf":
                        
                
                        logging.info(f"Extension {attachment.longFilename} not PDF")
                
                        if extension == '.docx' or extension == '.doc':

                            logging.info("Attachement extension is word")

                            name_attachement_pdf = os.path.join(self.folder, self.name + '.pdf')

                            convert_word_2_pdf(attachement_file_path, name_attachement_pdf)
                    
                            # Delete previous word document
                            os.remove(attachement_file_path)
                            attachement_file_path = name_attachement_pdf
                    
                        else:
                            logging.error(f"Unsupported extension {extension}")
                            raise Exception(f"Unsupported extension {extension}")

            else:
                logging.error(f"There is no attachement for {self.name}. Role={self.role}")
                raise Exception(f"There is no attachement for {self.name}. Role={self.role}")


        except Exception as e:
            logging.error(f"Error when getting resume of {self.name} in module Application.getResume(self, msg). Error={e}")
            raise Exception(f"Error when getting resume of {self.name} in module Application.getResume(self, msg). Error={e}")

        return attachement_file_path
   
    def save(self):

        engine = generate_engine()
        table_applications = os.environ['DB_TABLE_APPLICATIONS']

        insert_query = f"""
    INSERT INTO {table_applications} (score, Id, roleId, date,  name, role, experience, diplome, annee_diplome, certifications, hard_skills, soft_skills, langues, alternative_role, alternative_score, path) 
    VALUES (:score, :Id, :roleId, :date, :name, :role, :experience, :diplome, :annee_diplome, :certifications, :hard_skills, :soft_skills, :langues, :alternative_role, :alternative_score, :path);
    """

        # Define the values to insert
        values = {
        "score": self.score,
        "Id": self.Id,
        "roleId": self.roleId,
        "date": self.date,
        "name": self.name,
        "role": self.role,
        "experience": self.experience,
        "diplome": self.diplome,
        "annee_diplome": self.annee_diplome,
        "certifications": str(self.certifications),
        "hard_skills": str(self.hard_skills),
        "soft_skills": str(self.soft_skills),
        "langues": str(self.langues),
        "alternative_role": self.alternative_role,
        "alternative_score": self.alternative_score,
        "path": (self.pathResume).replace("\\", "/")

    }

        # Execute the insertion
        with engine.connect() as connection:
            with connection.begin():
                print(connection.execute(text(insert_query), values))
                logging.info(f"Saved application of {self.name} to database")

        return 0

    def scoring(self, required_experience, required_diplome):
        score_dipl = score_diplome(required_diplome, self.diplome) 
        logging.info(f"score_dipl={score_dipl}")
        score_exp = score_experience(required_experience, self.experience)
        logging.info(f"score_exp={score_exp}")
        self.score = int(0.3*score_dipl + 0.7*score_exp)
        logging.info(f"score={self.score}")
        return self.score
    



def convert_word_2_pdf(word_path, pdf_path):
    
    
    try:
        
        if not os.path.isfile(word_path):
            print(f"The word document does not exist {word_path}")
            raise Exception("Word document does not exists")
        convert(word_path, pdf_path)
        
    except Exception as e:
        print(e)
        raise Exception(e)


def value_diplome(diplome):
    logging.info(f"Calculating value of diplome={diplome}")

    if diplome==None:
        logging.error(f"The degree is None. diplome={diplome}")
        raise Exception("The degree is None. Check the value")
    elif diplome=="License" or diplome=="license" or diplome=="Bac+3" or diplome=="Bachelor":
        return 1.0
    elif str(diplome)=='Master' or diplome=="Bac+5" or diplome=="DEA" or diplome=="Master 2" or diplome=="Master 2" or diplome=="Diplôme d'ingénieur":
        return 2.0
    elif diplome=="Doctorat" or diplome=="PhD" or diplome=="Doctorate":
        return 3.0
    elif diplome=="Baccalaureat" or diplome=="baccalauréat" or diplome=="High school" or diplome=="High School":
        return 0.0
    else:
        logging.error(f"Invalid degree {diplome} in function value_diplome")
        raise Exception(f"Invalid degree {diplome} value_diplome")
        


def score_diplome(required_diplome, candidate_diplome):
    logging.info(" ")
    logging.info(" ")
    logging.info(f"Calculating score_diplome... ")
    logging.info(f"required_diplome={required_diplome} and candidate_diplome={candidate_diplome}")
    if value_diplome(candidate_diplome) >= value_diplome(required_diplome):
        return 100
    else:
        return 0

def score_experience(required_experience, candidate_experience):
    logging.info(" ")
    logging.info(" ")
    logging.info(f"Calculating score_experience... ")
    logging.info(f"required_experience={required_experience} and candidate_experience={candidate_experience}")

    score =  0.7* float(candidate_experience) / float(required_experience)
    if score >=1:
        score = 1
    score = 100*custom_exp(score)
    return score

def custom_exp(x):
    # Apply an exponential transformation that scales to fit the range [0, 1]
    return (np.exp(x) - 1) / (np.e - 1)



def selectApplication(roles, begin_date, end_date):

    selection = {}
    for role in roles:

        # We get all roles corresponding to role
        results = getApplication(role, begin_date, end_date)
        applications_list = []
        for result in results:
            application = Application(name=result['name'], score=result['score'],
            experience=result['experience'], date=result['date'], diplome=result['diplome'], annee_diplome=result['annee_diplome'],
            path=result['path'], certifications=result['certifications'], hard_skills=result['hard_skills'],
            soft_skills=result['soft_skills'], langues=result['langues'])
            applications_list.append(application)

        # Now we rank the applications by score
        for i in range(len(applications_list)):
            app1=applications_list[i]
            for j in range(len(applications_list)):
                app2=applications_list[j]
                if app1.score >= app2.score:
                    tampon = applications_list[i]
                    applications_list[i] = applications_list[j]
                    applications_list[j] = tampon

        selection[role] = applications_list

    return selection


def setLLM(llm_type=os.environ['LLM_TYPE']):

    from langchain_ollama.llms import OllamaLLM
    from langchain_openai import OpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.schema import AIMessage, HumanMessage

    if llm_type == "gpt-4-turbo":
        llm = ChatOpenAI(api_key=os.environ['OPENAI_API_KEY'], model="gpt-4-turbo", temperature=0)
        
    elif llm_type == "gpt-4":
        llm = OpenAI(api_key=os.environ['OPENAI_API_KEY'], model="gpt-4", temperature=0)

    elif llm_type == "openai":
        llm = OpenAI(api_key=os.environ['OPENAI_API_KEY'], temperature=0)

    elif llm_type == "llama3.2":
        llm = OllamaLLM(model="llama3.2", temperature=0.0)

    elif llm_type == "llama3.1":
        llm = OllamaLLM(model="llama3.1:8b", temperature=0.0)

    elif llm_type == "phi4":
        llm = OllamaLLM(model="phi4", temperature=0.0)

    elif llm_type == "deepseek-r1:8b":
        llm = OllamaLLM(model="deepseek-r1:8b", temperature=0.0) 

    elif llm_type == "deepseek14b":
        llm = OllamaLLM(model="deepseek-r1:14b", temperature=0.0) 

    elif llm_type == "qwen":
        llm = OllamaLLM(model="qwen2.5:7b", temperature=0.0)

    elif llm_type == "phi3.5:3.8b":
        llm = OllamaLLM(model="phi3.5:3.8b", temperature=0.0) 

    elif llm_type == "gemini":
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.environ['GOOGLE_API_KEY'])



    else:
        logging.info("Invalid llm")
        raise Exception("Invalid llm")

    return llm