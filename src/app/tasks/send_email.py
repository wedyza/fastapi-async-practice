import smtplib
from email.message import EmailMessage

from celery import shared_task
from jinja2 import Template
from starlette.templating import Jinja2Templates

from app.core.config import settings


@shared_task
def send_email_with_otp(to_email: str, otp: str) -> None:
    templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
    template: Template = templates.get_template(name="otp_email.html")
    html_content = template.render(otp=otp)

    message = EmailMessage()
    message.add_alternative(html_content, subtype="html")
    message["From"] = settings.EMAIL_SETTINGS.EMAIL_USER
    message["To"] = to_email
    message["Subject"] = "Одноразовый пароль для авторизации"

    with smtplib.SMTP_SSL(host=settings.EMAIL_SETTINGS.EMAIL_HOST, port = settings.EMAIL_SETTINGS.EMAIL_PORT) as smtp:
        smtp.login(
            user=settings.EMAIL_SETTINGS.EMAIL_USER,
            password=settings.EMAIL_SETTINGS.EMAIL_PASSWORD
        )
        smtp.send_message(message)
