import os
from celery import shared_task
from django.core.mail import send_mail

from config.celery import app


@app.task(bind=True)
def ecommerce_send_email(self, subject, message, recipient_list, *args, **kwargs):
    from_email = os.getenv('EMAIL_HOST_USER')
    print(subject, message, recipient_list)
    send_mail(subject, message, from_email, recipient_list)
    return f'Mail sent to {recipient_list}'
