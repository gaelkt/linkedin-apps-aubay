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

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Jesus Christ is my Savior")


from tasks import processMultipleApplications, processMultipleJobs

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

logging.info("Finish")

import sys
import shutil
import time
from celery.result import AsyncResult




