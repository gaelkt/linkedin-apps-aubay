# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 16:10:32 2025

@author: gaelk
"""
import os
from dotenv import load_dotenv
load_dotenv()

import mysql.connector

host=os.environ['DB_HOST'] 
port=os.environ.get("DB_PORT")
user=os.environ['DB_USER']
password=os.environ['DB_PASSWORD'] 
database_name=os.environ['DB_NAME']  
table_jobs = os.environ['DB_TABLE_JOB']  
table_applications = os.environ['DB_TABLE_APPLICATIONS'] 
table_scores = os.environ['DB_TABLE_SCORES']
table_tasks = os.environ['DB_TABLE_TASKS'] 
celery_table = os.environ['CELERY_TABLE_TASKS'] 

def fetch_applications_and_jobs(host=host, port=port, user=user, password=password, database_name=database_name):
    
    print(host)
    # Establish the connection
    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database_name
    )
    
    # Use dictionary=True so we can access columns by name
    cursor = connection.cursor(dictionary=True)

    # Step 1: Get all the application data we need
    query_applications = """
        SELECT Id, roleId, hard_skills, diplome, annee_diplome, experience
        FROM applications
    """
    cursor.execute(query_applications)
    applications = cursor.fetchall()
    
    results = []

    # Step 2: For each application, get the corresponding job
    query_job = """
        SELECT roleId, role, isActive, path, certifications, hard_skills, langues, soft_skills
        FROM jobs
        WHERE roleId = %s
    """
    
    for application in applications:
        cursor.execute(query_job, (application["roleId"],))
        job = cursor.fetchone()
        
        # You can store or process the data as needed.
        # Here we simply keep them together in a list of dicts
        results.append({
            "application": application,
            "job": job
        })

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return results

if __name__ == "__main__":


    data = fetch_applications_and_jobs(host, port, user, password, database_name)
    
    # Print the results or process them as needed
    count = 0
    for entry in data:
        application = entry["application"]
        job = entry["job"]
        # print('-------APP--------------')
        # print(application)
        # print('-------JOB--------------')
        # print(job)
        
        
        candidate_hard_skills = application['hard_skills']
        required_hard_skills = job['hard_skills']
        
        Nrequired = len(required_hard_skills)
        Nqualifications = len(candidate_hard_skills)
        
        C = [x for x in candidate_hard_skills if x in required_hard_skills]
        
        print(len(C))


        
        
        
        skill0 = candidate_hard_skills[0]
        count += 1
        
        if count == 1:
            break
