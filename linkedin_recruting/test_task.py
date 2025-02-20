import os
import sys
# Add the subfolders to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), './'))
sys.path.append(os.path.join(os.path.dirname(__file__), './llm'))
sys.path.append(os.path.join(os.path.dirname(__file__), './email'))
sys.path.append(os.path.join(os.path.dirname(__file__), './mysqldb'))

from mails import sendEmailGeneral
from libs import TaskCelery


import time
from celery.result import AsyncResult
from tasks import process_job_task
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

saved_paths = ["media/pdf_job/Consultant Data Power BI.pdf", "media/pdf_job/Consultant Data Qlik.pdf","media/pdf_job/ML Engineer.pdf"]

tasks = {}

# Lancer les tâches et stocker leur ID
for path in saved_paths:
    print(f"Processing {path}")
    result = process_job_task.delay(path, "gemini")
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
subject = "Toutes les tâches Celery sont terminées"
body = "Voici le résumé de l'exécution des tâches :\n\n"

for task_id, task_info in tasks.items():
    body += f"- Fichier : {task_info['path']}\n  Statut : {task_info['status']}\n  Résultat : {task_info['result']}\n\n"
    job_name = task_info['path'].split("/")[-1]
    if task_info["status"] == "SUCCESS":
         message = f"Successful process job {job_name}"
    else:
        message = f"Failed process job {job_name}"
    task = TaskCelery(
        Id=task_id,
        user="Gael",  # Assurez-vous que l'environnement USER est bien défini
        task_type="processing_jobs",
        date=datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        status=task_info["status"],
        message=message
    )
    
    task.save()

sendEmailGeneral(recipient_email="yiyuemej@yahoo.fr", message=body, subject=subject)


print("E-mail envoyé avec le résumé des tâches.")
