import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from libs import Application



from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib




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
