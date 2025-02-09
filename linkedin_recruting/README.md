# AI Recruiter Assistant Backend

## Getting started

This is an AI recruiter with the following capabilities:
- Analyze a given job description and extract the requirements such as experience needed, degree needed, etc..
- Read candidate applications, download resume, analyze it and extract candidate qualifications such as experience, degree, etc..
- Compare candidate qualifications with job requirements and calculate a matching score.

## Install Project
- [ ] You need to create an .env file with the necessary variables
```
pip install -r requirements.txt

```

## Start the project
- [ ] Start MySQL database and then run main.py
```
python main.py

```

## Endpoints

### Setup project Endpoint
Check database and create necessary tables
```
GET
http://localhost:8081/initialization
```

### View jobs Endpoint

View existing jobs in the database
```
GET
http://localhost:8081/view_jobs
```
Return a json where the keys are the roleId of different jobs and values json corresponding to job requirements
#### Example
```
{
    "3kyBidhu": {
        "role": "Tech Lead Data Engineering",
        "isActive": 1,
        "date": "2024-08-04",
        "path": "media/pdf_job/Tech Lead Data Engineering.pdf",
        "diplome": "Master",
        "experience": 5,
        "certifications": "[]",
        "hard_skills": "['Data Engineering', 'Big Data', 'Hadoop', 'Spark', 'Kafka', 'Kubernetes', 'Docker', 'Java']",
        "langues": "['anglais', 'francais']",
        "soft_skills": "['communication', 'écoute', 'collaboration', 'gestion de projet', 'leadership']"
    },
    "7hZ6glHq": {
        "role": "Generative AI Engineer",
        "isActive": 1,
        "date": "2024-09-16",
        "path": "media/pdf_job/Generative AI Engineer.pdf",
        "diplome": "Master",
        "experience": 5,
        "certifications": "[]",
        "hard_skills": "['Data Science', 'Intelligence Artificielle', 'Python', 'LLM', 'Retrieval-Augmented Generation', 'Chain-of-Thought', 'agents', 'frameworks']",
        "langues": "['anglais']",
        "soft_skills": "['communication orale et écrite de qualité', 'expert dans son domaine', 'capacité à préconiser le modèle le plus adapté', 'capacité à accompagner et soutenir techniquement', 'capacité à devenir un Lead']"
    }
}
```

### View applications Endpoint

\033[31mView existing applications in the database\033[0m
```
GET
http://localhost:8081/view_applications?begin_date=2024-05-01&end_date=2025-05-01&roles=ML Engineer&roles=Generative AI Engineer
```
Return a json where the keys are the role of different jobs and values a list of different candidates who applied to the job
#### Example
```
{
    "ML Engineer": [
        {
            "name": "Dat NGUYEN",
            "score": 51.0,
            "date": "2024-10-23",
            "experience": 3,
            "diplome": "Master",
            "certifications": "None",
            "hard_skills": "['Python', 'C++', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'SQL', 'PyTorch']",
            "soft_skills": "None",
            "langues": "None"
        },
        
        {
            "name": "Bilal El Hammouchi",
            "score": 36.0,
            "date": "2024-10-17",
            "experience": 1,
            "diplome": "Master",
            "certifications": "None",
            "hard_skills": "['Python', 'Java', 'JavaScript', 'C', 'Matlab', 'PySpark', 'Scikit-learn', 'TensorFlow']",
            "soft_skills": "None",
            "langues": "None"
        }
    ],
    "Generative AI Engineer": [
        {
            "name": "Moha Ameskour",
            "score": 51.0,
            "date": "2024-10-16",
            "experience": 3,
            "diplome": "Master",
            "certifications": "None",
            "hard_skills": "[\"Capacité d'Analyse\", \"Esprit d'Initiative\", 'Bon Relationnel', 'Python', 'R', 'C++', 'SAS', 'Hadoop']",
            "soft_skills": "None",
            "langues": "None"
        },
        
    ]
}
```
### Send report endpoint

Send an email report consisting of application between **begin_date** and **end_date** for the roles that are given in the request as a list. Several roles can be given in the request. A **recipient email** is also needed.

Inputs for the request below:
- **begin_date**:2024-05-01 
- **end_date** : 2025-01-01
- **roles**: [Data Engineer, ML Engineer, Generative AI Engineer]
- **recipient_email**:michel.kaham@aubay.com
```
GET
http://localhost:8081/report?begin_date=2024-05-01&end_date=2025-01-01&recipient_email=michel.kaham@aubay.com&roles=Data Engineer&roles=ML Engineer&roles=Generative AI Engineer
```


### Process Single Job Endpoint

Process a single job. Extract requirements and store them in database. Input should be pdf file path of the job. Input is **input_pdf_file** is the path of the pdf file where the job description is located
```
http://localhost:8081/single_job?input_pdf_file=C:\Users\gaelk\OneDrive\Desktop\Jobs\July 2023\python\jobanalysis\jobanalysis\media\pdf_job\Lead Power BI.pdf
```
It return a json with roleId, the role name of the job as well with a taskId representing the Id of the task that run that process:
```
{
    "role": "Lead Power BI",
    "roleId": "mIYDb0JL",
    "taskId": "YCawUghjdd"
}
```
Or
```
{
    "role": "Lead Power BI",
    "roleId": "mIYDb0JL",
    "taskId": "YCawUghjdd"
}
```

### Process Multiple Jobs Endpoint

Process multiple jobs. For each job, extract requirements and store them in database. Input should be the folder **pdf_jobs_folder** where pdf files are stored. If not given, then it take the default path in the .env file
```
GET
http://localhost:8081/multiple_jobs
```
Or 
```
GET
http://localhost:8081/multiple_jobs?pdf_jobs_folder=media/jobs_pdf
```

### Process Multiple Applications Endpoint

Endpoint used to process multiple applications and store their qualifications in the database.
Input: **email_folder**. Folder where emails applications are stored as a .msg files. If not given, we take the default email_folder in the .env file

```
http://localhost:8081/multiple_jobs?pdf_jobs_folder=media/jobs_pdf
```

### Notes for ongoing develoments
CASES WHERE WE HAVE SEVERAL ATTACHEMENTS (cover letter + resume)

FUNCTION generate_chunk_from_document TO BE WRITTEN BY ABDELAZIZ

CANDIDATURES QUI NE CORREPONDENT A AUCUN JOB OU A UN JOB MAL NOMME

CANDIDATURES AVEC TR

RANDOM GENERATION OF ROLEID

