from django.core.mail import send_mail
from celery import shared_task


# celery async function overload the default function 'django.core.mail.send_email'
send_email_celery = shared_task(send_mail, name='celery_async_send_email')
