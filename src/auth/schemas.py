import re
from ninja import Schema
from ninja.errors import HttpError
from pydantic import validator


class GoogleAuth(Schema):
    id: int = None
    token: str
    picture: str
    email: str


class GitHubAuth(Schema):
    code: str
    state: str


class Token(Schema):
    id: int
    token: str


class GitHubAccount(Schema):
    profile_id: int
    provider: str
    account_id: int
    account_url: str


class Email(Schema):
    username: str
    email: str
    password: str

    @validator('password')
    def check_password(cls, pw: str) -> str:
        if not bool(re.match(r'^(?=.*[0-9].*)', pw)):
            raise HttpError(400, "The password must be at least one number")
        elif not bool(re.match(r'^(?=.*[a-z].*)', pw)):
            raise HttpError(400, "The password must be at least one lowercase Latin letter")
        elif not bool(re.match(r'^(?=.*[A-Z].*)', pw)):
            raise HttpError(400, "The password must be at least one capital Latin letter")
        elif len(pw) < 8:
            raise HttpError(400, "The password must be at least 8 characters long")
        return pw

    @validator('email')
    def check_email(cls, email: str) -> str:
        if not bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)):
            raise HttpError(400, "Invalid Email")
        return email
