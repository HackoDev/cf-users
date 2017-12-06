from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_email_message(recipient, subject, html_content, text_content):
    """
    Email sending.
    
    :param recipient: list, str recipients
    :param subject: str Subject
    :param html_content: str HTML-body
    :param text_content: str Text-body
    :return: 
    """

    if not isinstance(recipient, (list, tuple)):
        recipient = [recipient]

    send_mail(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        recipient,
        html_message=html_content
    )
