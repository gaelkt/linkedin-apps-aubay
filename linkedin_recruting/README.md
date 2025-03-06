
# AI Recruiter Assistant Backend

  

## Getting started
This is the ReadMe for the backend.

The backend is developped with FastAPI. The backend can be run independently from the frontend. For example, you can use postman to send queries to the backend.

You will need an .env for environment variables.

The file main.py is the main file for the backend. Several endpoints have been developped for the backend:

- **@app.get("/initialization/")** to initialize the database and create all table. If you run the backend for the first time you need to call this endpoint first such that all tables can be created
- **@app.get("/view_jobs/")** to view existing jobs in the database.
- **@app.get("/view_applications/")** to view existing application in the database.
- **@app.post("/jobs/"**) to process one or several job descs. Jobs are sent as PDF files. You also need an email address where a notification will be sent once the processing is finished.
- **@app.post("/applications/")** to process one or several applications. Applications are sent as .msg files. You also need an email address where a notification will be sent once the processing is finished.
  

This is an AI recruiter with the following capabilities:

- Analyze a given job description and extract the requirements such as experience needed, degree needed, etc..

- Read candidate applications, download resume, analyze it and extract candidate qualifications such as experience, degree, etc..

- Compare candidate qualifications with job requirements and calculate a matching score.

  

## Install Project

- [ ] You need to create an **.env** file with the necessary variables
- [ ] If you install the project with docker, the backend will be installed automatically. But if you want to run the backend separetly without the frontend and without docker, create a python environment and in that environment do:

```
pip install -r requirements.txt
```
  
## Run the project

- [ ] First start your MySQL database
- [ ] Open two python consoles and activate your environment
- [ ] In the first console, start celery by running this command

```
celery -A celery_app worker -l info -Q aubay
```
- [ ] In the second console, start FastAPI by running this command:
  ```
python main.py
```
