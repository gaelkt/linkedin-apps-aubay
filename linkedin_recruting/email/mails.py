import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from libs import Application



from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import smtplib
import logging
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_EMAIL_SENDER = os.getenv("SMTP_EMAIL_SENDER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_HOST = os.getenv("SMTP_HOST")


def send(email, subject, body):
    try:
        # Configuration du message
        logging.info(f"Configure Email For {email}")
        
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL_SENDER
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        logging.info(f"Sending Email To {email}")
        
        
        if SMTP_HOST == "Dedicated":
            logging.info(f"Sending Email To {email} Using Dedicated SMTP Server")
            # Connexion au serveur SMTP DEDIE
            server = smtplib.SMTP(SMTP_SERVER)
            server.sendmail(SMTP_EMAIL_SENDER, email, msg.as_string())
            server.quit()
        else:
            # Connexion a un service SMTP classique
            logging.info(f"Sending Email To {email} Using  {SMTP_HOST} Server")
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_EMAIL_SENDER, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL_SENDER, email, msg.as_string())
            server.quit()

       

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")




def sendEmail(recipient_email, selection, topN=5):
    try:


        # Création du contenu de l'email
        
        logging.info(f"Formating Email Body")
        
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

        # Configuration du message
        logging.info(f"Called Function To Configure Email")
        send(recipient_email, subject, body)

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")


def sendEmailGeneral(recipient_email, message, subject):

    logging.info(f"Function sendEmailGeneral recipient_email={recipient_email}")

    if not is_valid_email(recipient_email):
        logging.error(f"Recipient email {recipient_email} is invalid in function sendEmailGeneral in file mails.py")
        raise Exception(f"Recipient email {recipient_email} is invalid")

    send(recipient_email, subject, message)
 

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
        <p>Below is a summary of the processed applications:</p>
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
        <p>Please review any failed applications and take the necessary actions.</p>
        <p>Thank you for your attention to this matter.</p>
        <p>Best regards,<br>Aubay AI Recruiter Assistant</p>
    </body>
    </html>
    """

    # Check if the email is valid or not
    if not is_valid_email(recipient_email):
        logging.error(f"Recipient email {recipient_email} is invalid in function sendEmailGeneral in file mails.py")
        raise Exception(f"Recipient email {recipient_email} is invalid")

    send(recipient_email, subject, email_content_html)
    
    


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

    send(recipient_email, subject, email_content_html)
    
    
    



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
