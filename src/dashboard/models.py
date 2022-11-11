from django.db import models
from django.utils import timezone

from src.profiles.models import Profile
from src.repository.models import Project


class Board(models.Model):
    """ Модель доски заданий
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='board')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=50, blank=True, null=True)


class Column(models.Model):
    """ Модель столбцов в доске заданий
    """
    boardId = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    position = models.IntegerField(default=0)
    title = models.CharField(max_length=50)


class Card(models.Model):
    """ Модель карточек в доске заданий
    """
    listId = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='cards')
    position = models.IntegerField(default=0)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField(default=timezone.now)
    labels = models.ManyToManyField('Label', blank=True, null=True)
    members = models.ManyToManyField(Profile, related_name='cards_member', blank=True, null=True)


class Label(models.Model):
    """ Модель меток в доске заланий
    """
    boardId = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='labels')
    title = models.CharField(max_length=50)
