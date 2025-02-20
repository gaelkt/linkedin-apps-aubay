from fastapi import FastAPI, HTTPException # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from pydantic import BaseModel # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
from langchain.chains import create_sql_query_chain # type: ignore
from langchain_community.utilities import SQLDatabase # type: ignore
# from langchain.agents import create_sql_agent # type: ignore
from langchain_community.agent_toolkits.sql.base import create_sql_agent

# from langchain.agents.agent_toolkits import SQLDatabaseToolkit # type: ignore
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine # type: ignore
from openai import OpenAI # type: ignore
import pymysql # type: ignore
from sqlalchemy import create_engine, text # type: ignore
from sqlalchemy.engine import Row # type: ignore
from libs import setLLM


from dotenv import load_dotenv # type: ignore
import sys
import os
load_dotenv()

class ChatRequest(BaseModel):
    query: str

conversation_history = []
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY")
)

user=os.environ.get("DB_USER")
host=os.environ.get("DB_HOST")
password=os.environ.get("DB_PASSWORD")
database=os.environ.get("DB_NAME")
port=os.environ.get("DB_PORT")
llm_type=os.environ.get("LLM_TYPE")

def validate_and_clean_query(query: str) -> str:
    # Supprimer tout point-virgule mal placé
    
    cleaned_query = query.replace(';', '').strip()
    cleaned_query = cleaned_query.replace('`', '').strip()
    cleaned_query = cleaned_query.replace('sql', '').strip()
    # Ajout du point-virgule uniquement à la fin
    if not cleaned_query.endswith(';'):
        cleaned_query += ';'
    return cleaned_query

def getData(query:str):
    query = validate_and_clean_query(query)
    database_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    print("DEBUG: Receive SQL Query:")
    print("------------")
    print(query)
    engine = create_engine(database_url)
    with engine.connect() as connection:
      with connection.begin():
        result=connection.execute(text(query)).fetchall()
        print("DEBUG: Raw result:", result)
        return [row._asdict() if isinstance(row, Row) else dict(row) for row in result]
      


def langchain_agent(query):
    try:
        db = SQLDatabase.from_uri(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
        #llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        llm=setLLM(llm_type)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
        response = agent.run(query)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def langchain_agent_sql(query):
    try:
        db = SQLDatabase.from_uri(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
        llm=setLLM(llm_type)
        #llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        chain = create_sql_query_chain(llm, db)
        sql_query = chain.invoke({"question": query})
        print("DEBUG: Generated SQL Query:", sql_query)
        response = getData(sql_query)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    