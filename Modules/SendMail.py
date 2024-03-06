import json
import smtplib
from email.message import EmailMessage
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def SendMail(Subject: str, Body: str, Attachment: str):
    try:
        # Lire le fichier de configuration
        with open('./Config/MailConfig.json', 'r') as file:
            Email = json.load(file)
        
        Msg = EmailMessage()
        Msg['Subject'] = Subject
        Msg['From'] = Email['user']
        # Divisez la chaîne des destinataires en liste si nécessaire
        Msg['To'] = Email['to'].split(',')  # S'il y a plusieurs destinataires
        Msg.set_content(Body)
        
        with open(Attachment, 'rb') as File:
            Data = File.read()
            FileName = File.name
        Msg.add_attachment(Data, maintype='application', subtype='octet-stream', filename=FileName)
        
        logger.info('Sending email...')
        with smtplib.SMTP_SSL(Email['host'], Email['port']) as Server:
            Server.login(Email['user'], Email['password'])
            Server.send_message(Msg)
        logger.info('Email sent successfully')
        
    except Exception as error:
        logger.error('Failed to send email', exc_info=True)
        raise error

# Exemple d'utilisation
#SendMail('Test Subject', 'This is the body of the email', 'path/to/your/attachment.txt')
