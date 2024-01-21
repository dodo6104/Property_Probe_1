from email.message import EmailMessage
import ssl
import smtplib
import datafunctions

def sendMail(body):

    email_sender = 'yourname'
    email_password = 'nyoutpassword'
    email_receaver = datafunctions.returnDataForMail("B1")

    subject = datafunctions.returnDataForMail("B2")

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receaver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receaver, em.as_string())