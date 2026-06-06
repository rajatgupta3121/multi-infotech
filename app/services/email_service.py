from flask_mail import Message
from flask import current_app
from app.extensions import mail


def send_lead_email(name, email, phone, message):

    msg = Message(
        subject="New Lead 🚀",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[current_app.config["MAIL_DEFAULT_SENDER"]]
    )

    msg.body = f"""
New Lead Received

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
"""

    mail.send(msg)