import httpx
from typing import Optional

import requests
from ninja.errors import HttpError
from config.settings import (
    GITHUB_CLIENT_ID, GITHUB_SECRET_KEY, GITHUB_SECRET_KEY_AUTH, GITHUB_CLIENT_ID_AUTH
)
from . import tokenizator
from src.profiles.services import account_service
from ...profiles.models import Profile


def check_github_token_add_acc(code: str, state: str) -> str:
    url_token = 'https://github.com/login/oauth/access_token'
    data = {
        "code": code,
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_SECRET_KEY,
        "stat": state
    }
    check = requests.post(url_token, data=data)
    _token = check.text.split("&")[0].split("=")[1]
    return _token


def check_github_token_auth(code: str, state: str) -> str:
    url_token = 'https://github.com/login/oauth/access_token'
    data = {
        "code": code,
        "client_id": GITHUB_CLIENT_ID_AUTH,
        "client_secret": GITHUB_SECRET_KEY_AUTH,
        "stat": state
    }
    check = requests.post(url_token, data=data)
    _token = check.text.split("&")[0].split("=")[1]
    return _token


def check_github_user(_token):
    url_check_user = 'https://api.github.com/user'
    headers = {'Authorization': f'token {_token}'}
    user = requests.get(url_check_user, headers=headers)
    return user


def check_github_auth(code: str, state: str) -> Optional[dict]:
    _token = check_github_token_auth(code, state)
    if _token != 'bad_verification_code':
        user = check_github_user(_token)
        return user.json()
    return None


def check_github_add(code: str, state: str) -> Optional[dict]:
    _token = check_github_token_add_acc(code, state)
    if _token != 'bad_verification_code':
        user = check_github_user(_token)
        return user.json()
    return None


def github_auth(code: str, state: str) -> tuple:
    user = check_github_auth(code, state)
    if user is not None:
        user_id = account_service.GitHub(user).authorize_user()
        internal_token = tokenizator.create_token(user_id)
        return user_id, internal_token
    else:
        raise HttpError(403, "Bad code")


def add_account_github(code: str, state: str, user: Profile):
    _user = check_github_add(code, state)
    if _user:
        return account_service.GitHub(_user, user.id).add_account()
    else:
        raise HttpError(403, "Bad code")
