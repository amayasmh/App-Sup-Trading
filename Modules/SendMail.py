import json
import smtplib
from email.message import EmailMessage



def send_mail(subject: str, body: str, attachment: str):
    """
    Envoie un email avec un sujet, un corps de message et une pièce jointe.

    :param subject: Sujet de l'email.
    :param body: Corps du message de l'email.
    :param attachment: Chemin vers le fichier à attacher à l'email.
    """
    try:
        # Lire le fichier de configuration des détails de l'email.
        with open('./Config/MailConfig.json', 'r') as file:
            emailConfig = json.load(file)
        
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = emailConfig['user']
        # Si les destinataires sont multiples, ils sont séparés par une virgule dans la configuration.
        msg['To'] = emailConfig['to'].split(',')  # Transforme la chaîne des destinataires en liste
        msg.set_content(body)
        
        # Attache le fichier spécifié à l'email.
        with open(attachment, 'rb') as file:
            data = file.read()
            fileName = file.name
        msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=fileName)
        
        
        with smtplib.SMTP_SSL(emailConfig['host'], emailConfig['port']) as server:
            server.login(emailConfig['user'], emailConfig['password'])
            server.send_message(msg)
        
        print("Email envoyé avec succès.")
        
    except Exception as error:
       
        print("Echec de l\'envoi de l\'email.")
        raise error
