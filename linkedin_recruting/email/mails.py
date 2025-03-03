import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from libs import Application



from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import smtplib
import logging




def sendEmail(recipient_email, selection, topN=5):
    try:


        # Création du contenu de l'email
        subject = f"Job board summary"
        body = """
        <html>
        <head>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
        """
        body+=f"""
        Bonjour, <br/>
        Veuillez trouver ci-dessous la liste des candidats ayant postulé chez Aubay.
        """

        # Génération des tableaux pour chaque IDJob
        for role in selection:
            body += f"<h2> {role} </h2>"
            body += """
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Score</th>
                        <th>Experience</th>
                        <th>Date</th>
                        
                    </tr>
                </thead>
                <tbody>
            """

            # Prendre uniquement les topN candidats
            # top_candidates = candidates[:topN]

            for candidate in selection[role]:
                body += f"""
                    <tr>
                        <td>{candidate.name}</td>
                        <td>{candidate.score}</td>
                        <td>{candidate.experience}</td>
                        <td>{candidate.date}</td>
                      
                    </tr>
                """

            body += """
                </tbody>
            </table>
            <br/>


            
            """

        body += """
        Cordialement,
        L'assistant AI
        </body>
        </html>
        """


        deliverEmail(subject=subject, email_content_html=body, recipient_email=recipient_email)


    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")


def sendEmailGeneral(recipient_email, message, subject):

    logging.info(f"Function sendEmailGeneral recipient_email={recipient_email}")

    if not is_valid_email(recipient_email):
        logging.error(f"Recipient email {recipient_email} is invalid in function sendEmailGeneral in file mails.py")
        raise Exception(f"Recipient email {recipient_email} is invalid")


    deliverEmail(subject=subject, email_content_html=message, recipient_email=recipient_email)

    backupContent(recipient_email, message)

    
    return 0
    

def computeEmailApplication(recipient_email:str, applications_received:int,
    applications_processed:int, application_success:int, output_log):


    logging.info(f"Function computeEmailApplication recipient_email={recipient_email}")
    
    subject = f"Automated report for the processing of {applications_received} application(s)"

    logging.info(f"Subject of email={subject}")
    
    email_content_html = f"""
    <html>
    <head>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 10px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <p><strong>Subject:</strong> Automated Job Application Processing Report</p>
        <p>Dear HR Team,</p>
        <p>I hope this message finds you well.</p>
        <p>Please find below an automated report for today’s job application processing:</p>
        <ul>
            <li><strong>Total number of applications received :</strong> {applications_received}</li>
            <li><strong>Number of applications processed:</strong> {applications_processed}</li>
            <li><strong>Number of applications processed successfully:</strong> {application_success}</li>
        </ul>
        <p>Below is a summary of the applications that did not succeed:</p>
        <table>
           <thead>
              <tr>
                 <th>Filename</th>
                 <th>Status</th>
                 <th>Description</th>
              </tr>
            </thead>
            <tbody>
            
            """
    for log in output_log:
        email_content_html += f"""
            <tr>
                <td>{log['filename']}</td>
                <td>{log['status']}</td>
                <td>{log['description']}</td>
            </tr>
        """
    email_content_html += f"""
    
            </tbody>
            
        </table>
        <p>Please review these applications and take the necessary actions.</p>
        <p>Thank you for your attention to this matter.</p>
        <p>Best regards,<br>Aubay AI Recruiter Assistant</p>
    </body>
    </html>
    """

    # Check if the email is valid or not
    if not is_valid_email(recipient_email):
        logging.error(f"Recipient email {recipient_email} is invalid in function sendEmailGeneral in file mails.py")
        raise Exception(f"Recipient email {recipient_email} is invalid")

    deliverEmail(subject=subject, email_content_html=email_content_html, recipient_email=recipient_email)
    
    content = str({"task": "computeEmailApplication", "applications_received":applications_received,
    "applications_processed":applications_processed, "application_success":application_success, "output_log":output_log})

    backupContent(recipient_email, email_content_html)
    
    


def computeEmailJob(recipient_email:str, jobs_received:int,
    jobs_processed:int, jobs_success:int, output_log):


    logging.info(f"Function computeEmailJob recipient_email={recipient_email}")
    
    subject = f"Automated report for the processing of {jobs_received} job desc(s)"

    logging.info(f"Subject of email={subject}")
    
    email_content_html = f"""
    <html>
    <head>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 10px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <p>Dear HR Team,</p>
        <p>I hope this message finds you well.</p>
        <p>Please find below an automated report for today’s job desc processing:</p>
        <ul>
            <li><strong>Total number of job descs received :</strong> {jobs_received}</li>
            <li><strong>Number of job descs processed:</strong> {jobs_processed}</li>
            <li><strong>Number of job descs processed successfully:</strong> {jobs_success}</li>
        </ul>
        <p>Below is a summary of the processed job descs:</p>
        <table>
           <thead>
              <tr>
                 <th>Filename</th>
                 <th>Status</th>
                 <th>Description</th>
              </tr>
            </thead>
            <tbody>
            
            """
    for log in output_log:
        email_content_html += f"""
            <tr>
                <td>{log['filename']}</td>
                <td>{log['status']}</td>
                <td>{log['description']}</td>
            </tr>
        """
    email_content_html += f"""
    
            </tbody>
            
        </table>
        <p>Please review any failed job descs and take the necessary actions.</p>
        <p>Thank you for your attention to this matter.</p>
        <p>Best regards,<br>Aubay AI Recruiter Assistant</p>
    </body>
    </html>
    """

    # Check if the email is valid or not
    if not is_valid_email(recipient_email):
        logging.error(f"Recipient email {recipient_email} is invalid in function sendEmailGeneral in file mails.py")
        raise Exception(f"Recipient email {recipient_email} is invalid")

    deliverEmail(subject=subject, email_content_html=email_content_html, recipient_email=recipient_email)


    content = str({"task": "jobs_processed", "jobs_received":jobs_received,
    "jobs_processed":jobs_processed, "jobs_success":jobs_processed, "output_log":output_log})

    backupContent(recipient_email, email_content_html)
    


    return 0
        
    
    



def is_valid_email(email: str) -> bool:
    """
    Check if the provided email is in a valid format.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    # This regex matches most common email patterns.
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email) is not None



def deliverEmail(subject, email_content_html, recipient_email):

    try:

        msg = MIMEMultipart()
        

        # Connexion au serveur SMTP 
        logging.info("")
        if os.environ['PLATFORM'] != "windows":
            logging.info(f"We are not on Windows")

            # Email settings
            msg['From'] = os.environ['APPLICATION_EMAIL']
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(email_content_html, 'html'))

            # Smtp server
            server = smtplib.SMTP(os.environ['SMTP_SERVER'])
            server.sendmail(os.environ['APPLICATION_EMAIL'], recipient_email, msg.as_string())  
        else:
            logging.info("We are on Windows ...")

            # Email settings
            msg['From'] = "gaelkamdem@yahoo.fr"
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(email_content_html, 'html'))

            # Smtp server
            logging.info("Prapring smtp server ...")
            server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
            logging.info("smtp configured with smtp.mail.yahoo.com and port 587")
            server.starttls()
            logging.info("smtp started")
            server.login('gaelkamdem@yahoo.fr', 'nzszqfqetawnqkch')
            logging.info("logging ok")
            server.sendmail('gaelkamdem@yahoo.fr', recipient_email, msg.as_string())
        
        logging.info(f"Email sent to {recipient_email}")
        server.quit()   
        logging.info("Server quit")
        
    except Exception as e:
        logging.info(f"Unable to send email to {recipient_email}")
        logging.error(e)
        

    return 0



def backupContent(recipient_email, content):

    try:

        deliverEmail(recipient_email, content, os.environ['BACKUP_RECIPIENT_EMAIL'])
    except Exception as e:
        logging.info(e)
    return 0
