from tasks import process_job_task

path_files = ["media/pdf_job/Tech Lead Data Engineering.pdf", "media/pdf_job/Data Solutions Architect.pdf"]

status = []

for path in path_files:
    print(f"Processing {path}")
    result = process_job_task.delay(path, "openai")
    print(result.id)
    print(result.status)
    
    