from typing import Optional

from django.contrib.auth.hashers import make_password, check_password
from ninja.errors import HttpError

from src.profiles.models import Profile, Account, AccountEmail, VerifyEmail
from src.auth import schemas


class BaseService:
    def __init__(
            self,
            provider: str,
            username: str,
            email: str = None,
            account_name: str = None,
            account_id: int = None,
            account_url: str = '',
            profile_pk: int = None
    ):
        self._user: Optional[Profile] = None
        self._provider = provider
        self._username = username
        self._account_name = account_name
        self._account_id = account_id
        self._account_url = account_url
        self._email = email
        self._login = f'{self._provider}-{self._username}'
        self._profile_pk = profile_pk

    def _get_user(self, **kwargs) -> None:
        self._user = Profile.objects.get(**kwargs)

    def _create_user(self, is_active=True):
        counter = 1
        while Profile.objects.filter(username=self._username).exists():
            username = self._username + str(counter)
            counter += 1
            self._username = username

        self._user = Profile.objects.create(
            username=self._username,
            email=self._email,
            github=self._account_url,
            is_active=is_active
        )

    def _update_user(self) -> None:
        self._user.github = self._account_url
        self._user.save()

    def _create_account(self):
        return Account.objects.create(
            username=self._login,
            profile=self._user,
            provider=self._provider,
            account_id=self._account_id,
            account_url=self._account_url,
            account_name=self._account_name,
        )

    def _get_or_create_account(self) -> Account:
        try:
            _acc = Account.objects.select_related('profile').get(username=self._login)
            self._user = _acc.profile
        except Account.DoesNotExist:
            self._create_user()
            _acc = self._create_account()
        return _acc

    def authorize_user(self) -> int:
        self._get_or_create_account()
        return self._user.id

    def add_account(self) -> Optional[Account]:
        self._get_user(id=self._profile_pk)
        try:
            _acc = Account.objects.get(provider=self._provider, profile=self._user)
        except Account.DoesNotExist:
            _acc = self._create_account()
        self._update_user()
        return _acc


class Google(BaseService):
    def __init__(self, user: schemas.GoogleAuth):
        super().__init__(
            provider="Google",
            username=user.email.split(sep='@')[0],
            email=user.email,
            account_name=user.email.split(sep='@')[0],
            account_id=user.id
        )


class GitHub(BaseService):
    def __init__(self, user: dict, profile_pk: int = None):
        super().__init__(
            provider="GitHub",
            username=user['login'],
            account_name=user['login'],
            account_id=user['id'],
            account_url=user['html_url'],
            profile_pk=profile_pk
        )


class Email(BaseService):
    def __init__(self, email: str, password: str, username: str = None):
        super().__init__(
            provider="Email",
            username=username,
            email=email,
        )
        self._password = password
        self._hash_password = None

    _raw_pass = None

    def set_password(self, raw_password):
        self._hash_password = make_password(raw_password)
        self._raw_pass = raw_password

    def check_verify(self, token):
        try:
            verify = VerifyEmail.objects.get(token=token)
            self._get_user(id=verify.profile_id)
            self._user.is_active = True
            self._user.save()
            verify.delete()
        except VerifyEmail.DoesNotExist:
            raise HttpError(404, "Not found")

    def registration(self):
        if AccountEmail.objects.filter(email=self._email).exists():
            raise HttpError(403, "User with this email already exists")
        if Profile.objects.filter(username=self._username).exists():
            raise HttpError(403, "User with this name already exists")

        self._create_user(is_active=False)
        self.set_password(self._password)
        AccountEmail.objects.create(
            email=self._email, profile=self._user, password=self._hash_password
        )
        return VerifyEmail.objects.create(profile=self._user)

    def authorize_user(self) -> int:
        try:
            acc_email = AccountEmail.objects.select_related('profile').get(email=self._email)
        except AccountEmail.DoesNotExist:
            raise HttpError(403, "Invalid email")

        if not check_password(self._password, acc_email.password):
            raise HttpError(403, "Invalid password")

        if acc_email.profile.is_active:
            return acc_email.profile.id
        else:
            raise HttpError(403, "Email not confirmed")


