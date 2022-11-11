from django.db import models

from src.profiles.models import Profile


class Follower(models.Model):
    """ Модель подписчиков
    """
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    subscriber = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )

    def __str__(self):
        return f"{self.subscriber} follower {self.user}"
