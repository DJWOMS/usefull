from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any

import jwt
from jwt import PyJWTError
from django.http import HttpRequest
from django.conf import settings
from ninja.compatibility import get_headers
from ninja.security.http import HttpAuthBase
from rest_framework.generics import get_object_or_404

from src.profiles.models import Profile

ALGORITHM = "HS256"


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except PyJWTError:
        return None

    token_exp = datetime.fromtimestamp(payload['exp'])
    if token_exp < datetime.utcnow():
        return None

    return get_object_or_404(Profile, id=payload['user_id'])


class Auth(HttpAuthBase, ABC):
    openapi_scheme: str = "token"
    header: str = "Authorization"

    def __call__(self, request: HttpRequest) -> Optional[Any]:
        headers = get_headers(request)
        auth_value = headers.get(self.header)
        if not auth_value:
            return None
        parts = auth_value.split(" ")

        if parts[0].lower() != "token":
            return None
        token = " ".join(parts[1:])
        return self.authenticate(request, token)

    @abstractmethod
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        pass


class AuthToken(Auth):
    def authenticate(self, request, token: str) -> Profile:
        user = get_current_user(token)
        if user:
            return user
