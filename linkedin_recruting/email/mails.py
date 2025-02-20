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

        # Configuration du message
        msg = MIMEMultipart()
        msg['From'] = "gaelkamdem@yahoo.fr"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connexion au serveur SMTP Yahoo
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login('gaelkamdem@yahoo.fr', 'nzszqfqetawnqkch')
        server.sendmail('gaelkamdem@yahoo.fr', recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")


def sendEmailGeneral(recipient_email, message, subject):

    logging.info(f"Function sendEmailGeneral recipient_email={recipient_email}")

    if not is_valid_email(recipient_email):
        logging.error(f"Recipient email {recipient_email} is invalid in function sendEmailGeneral in file mails.py")
        raise Exception(f"Recipient email {recipient_email} is invalid")

    try:

        msg = MIMEMultipart()
        msg['From'] = "gaelkamdem@yahoo.fr"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))

        # Connexion au serveur SMTP Yahoo
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login('gaelkamdem@yahoo.fr', 'nzszqfqetawnqkch')
        server.sendmail('gaelkamdem@yahoo.fr', recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        logging.info(f"Impossible to send email in function sendEmailGeneral. Error = {e}")
        raise Exception(e)
    


def computeEmailApplication(recipient_email:str, applications_received:int,
    applications_processed:int, output_log):


    logging.info(f"Function sendEmailGeneral recipient_email={recipient_email}")
    
    subject = f"Processing of New  {applications_received} Application(s)"
    
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
        <p>This is an automated report regarding the job application processing for today. Below are the details:</p>
        <ul>
            <li><strong>Total Applications Processed:</strong> {applications_received}</li>
            <li><strong>Successfully Processed:</strong> {applications_processed}</li>
            <li><strong>Failed Processing:</strong> {applications_received - applications_processed}</li>
        </ul>
        <p>Please find below a summary table of the processed applications:</p>
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
        <p>Please review the failed applications and take the necessary actions.</p>
        <p>Thank you for your attention to this matter.</p>
        <p>Best regards,<br>Aubay AI Recruiter Assistant</p>
    </body>
    </html>
    """

    # Check if the email is valid or not
    if not is_valid_email(recipient_email):
        logging.error(f"Recipient email {recipient_email} is invalid in function sendEmailGeneral in file mails.py")
        raise Exception(f"Recipient email {recipient_email} is invalid")

    try:
    
    # Edit this part to have an HTML email with a body
        

        msg = MIMEMultipart()
        msg['From'] = "gaelkamdem@yahoo.fr"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(email_content_html, 'html'))

        # Connexion au serveur SMTP Yahoo
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login('gaelkamdem@yahoo.fr', 'nzszqfqetawnqkch')
        server.sendmail('gaelkamdem@yahoo.fr', recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        logging.info(f"Impossible to send email in function sendEmailGeneral. Error = {e}")
        raise Exception(e)
    
    
    

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
