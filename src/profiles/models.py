import uuid

from django.core.validators import FileExtensionValidator
from django.db import models


class Profile(models.Model):
    """ User """
    GENDER = (
        ('male', 'male'),
        ('female', 'female')
    )
    username = models.CharField(unique=True, max_length=250)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='user/avatar/',
        default='/default/default.jpg',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg'])]
    )
    bio = models.TextField(blank=True, null=True)
    github = models.CharField(max_length=500, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER, default='male')
    technology = models.ManyToManyField(
        'Technology',
        related_name='users'
    )
    achievement = models.ManyToManyField(
        'achievements.Achievement',
        related_name='users',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    def subscribers_count(self):
        return self.subscribers.count()

    def subscription_count(self):
        return self.owner.count()

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


class Technology(models.Model):
    """ Technology model
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return self.name


class Account(models.Model):
    """ Social account user """
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    provider = models.CharField(max_length=25)
    username = models.CharField(max_length=150, unique=True)
    account_email = models.CharField(max_length=150, blank=True, null=True)
    account_id = models.CharField(max_length=150, blank=True, null=True)
    account_url = models.CharField(max_length=250, default='')
    account_name = models.CharField(max_length=250, default='')


class AccountEmail(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='account_email'
    )
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=128)


class VerifyEmail(models.Model):
    """ Email verify """
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='verify'
    )
    token = models.UUIDField(default=uuid.uuid4)


class ColorSchema(models.Model):
    """ Схема выбранная на frontend
    """
    user = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='color_schema'
    )
    theme = models.CharField(max_length=50, default='default')
    scheme = models.CharField(max_length=50, default='light')
    layout = models.CharField(max_length=50, default='classy')
