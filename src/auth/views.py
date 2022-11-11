from django.shortcuts import render
from django.views.generic.base import View
from ninja import Router, Form
from . import schemas
from .base_auth import AuthToken
from .services import google_service, github

from .services.email import sign_up, confirm, email_auth

auth = Router()


class LoginGoogle(View):
    def get(self, request):
        return render(request, 'auth/i.html')


@auth.post("/google/auth", response=schemas.Token)
def auth_google(request, user: schemas.GoogleAuth):
    user_id, token = google_service.google_auth(user)
    return schemas.Token(id=user_id, token=token.get("access_token"))


@auth.post("/github/auth", response=schemas.Token)
def auth_github(request, github_code: schemas.GitHubAuth):
    user_id, token = github.github_auth(github_code.code, github_code.state)
    return schemas.Token(id=user_id, token=token.get("access_token"))


@auth.post("/github/add", response=schemas.GitHubAccount, auth=AuthToken())
def add_github_account(request, github_code: schemas.GitHubAuth):
    return github.add_account_github(github_code.code, github_code.state, request.auth)


@auth.post("/registration")
def registration(request, data: schemas.Email = Form(...)):
    sign_up(data.email, data.password, data.username)
    return 200, {'message': 'Send mail'}


@auth.post("/confirm_email")
def confirm_email(request, token: str = Form(...)):
    confirm(token)
    return 200, {'message': 'Verified email'}


@auth.post("/login", response=schemas.Token)
def login(request, email: str = Form(...), password: str = Form(...)):
    user_id, token = email_auth(email, password)
    return schemas.Token(id=user_id, token=token.get("access_token"))


@auth.get("/chek-auth", auth=AuthToken())
def check_auth(request):
    if request.auth:
        return 200, {'message': 'OK'}
    return 401, {'message': 'Unauthorized'}
