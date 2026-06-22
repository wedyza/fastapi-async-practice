from .asleep import asleep
from .send_email import send_email_with_otp

__all__ = ['asleep', 'send_email_with_otp']

TASKS = [
    send_email_with_otp, asleep
]
