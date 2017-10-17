from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_email_message(recipient, subject, html_content, text_content):
    """
    Отправка email-сообщения.
    
    :param recipient: list or str Список email адресов
    :param subject: str Тема сообщения
    :param html_content: str HTML тело
    :param text_content: str Текстовое тело
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
