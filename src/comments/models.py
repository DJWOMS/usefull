from django.db import models

from src.profiles.models import Profile


class AbstractComment(models.Model):
    """Абстрактная модель комментариев"""
    text = models.TextField(max_length=512)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_publish = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        abstract = True
