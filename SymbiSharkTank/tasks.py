from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta, datetime
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def simple_task(a, b):
    return a + b

@shared_task
def send_mail_after_delay(email, message, email_host_user, email_host_password):
    try:
        print(f"Email: {email}, Message: {message}, User: {email_host_user}, Password: {email_host_password}")
        send_mail(
            'Round 1 Results',
            message,
            email_host_user,
            [email],
            fail_silently=False,
            auth_user=email_host_user,
            auth_password=email_host_password
        )
        return "Email sent successfully."
    except Exception as e:
        # Log the exception or handle it as necessary
        logger.error(f"Error sending email: {str(e)}")
        return f"Failed to send email: {str(e)}"
    

@shared_task
def test_task(arg1, arg2):
    return f"Received arguments: {arg1}, {arg2}"

