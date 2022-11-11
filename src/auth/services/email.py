from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from src.auth.services import tokenizator
from src.base.send_mail import send_email
from src.profiles.services.account_service import Email


def send_verify_mail(email, token):
    template = get_template('auth/email_template/email_template.html')
    content = template.render(
        {
            'link': f"{settings.SERVER_HOST}confirm/{token}",
            'host': f"{settings.SERVER_HOST}",
        }
    )
    message = send_email(
        from_email='robot@collabteam.dev',
        to_emails=email,
        subject='Welcome to Collab Team! Confirm Your Email',
        html_content=content
    )


def sign_up(email: str, password: str, username: str):
    verify = Email(email, password, username).registration()
    send_verify_mail(email, verify.token)


def confirm(token: str):
    Email('username', 'email', 'password').check_verify(token)


def email_auth(email: str, password: str) -> tuple:
    user_id = Email(email, password).authorize_user()
    internal_token = tokenizator.create_token(user_id)
    return user_id, internal_token
