import smtplib
from email.message import EmailMessage

EMAIL = "lollo.la@alice.it"
PASSWORD = "19052001"

def send_email(subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.alice.it", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
