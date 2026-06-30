from .asleep import asleep
from .fetch import fetch
from .send_email import send_email_with_otp

__all__ = ['asleep', 'fetch', 'send_email_with_otp']

TASKS = [
    send_email_with_otp, asleep, fetch
]
