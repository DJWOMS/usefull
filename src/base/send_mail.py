from rest_framework import exceptions
from django.core.mail import send_mail, BadHeaderError


def send_email(
        from_email='robot@collabteam.dev',
        to_emails='',
        subject='Collab Team',
        html_content='<strong>/strong>'
):
    try:
        send_mail(
            subject=subject,
            message=html_content,
            from_email=from_email,
            recipient_list=[to_emails],
            html_message=html_content
        )
    except BadHeaderError:
        raise exceptions.APIException(detail='Send mail error', code=400)
