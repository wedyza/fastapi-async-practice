import smtplib
from email.message import EmailMessage
from pathlib import Path

from fastapi.templating import Jinja2Templates
from jinja2 import Template

from src.app.core.config import settings


async def send_email_with_otp(ctx: ..., to_email: str, otp: str) -> None:
    BASE_DIR = Path(__file__).parent.parent
    templates = Jinja2Templates(directory=BASE_DIR / "templates")
    template: Template = templates.get_template(name="otp_email.html")
    html_content = template.render(otp=otp)

    message = EmailMessage()
    message.add_alternative(html_content, subtype="html")
    message["From"] = settings.EMAIL_SETTINGS.EMAIL_USER
    message["To"] = to_email
    message["Subject"] = "Одноразовый пароль для авторизации"

    with smtplib.SMTP(host=settings.EMAIL_SETTINGS.EMAIL_HOST, port = settings.EMAIL_SETTINGS.EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(
            user=settings.EMAIL_SETTINGS.EMAIL_USER,
            password=settings.EMAIL_SETTINGS.EMAIL_PASSWORD
        )
        smtp.send_message(message)
