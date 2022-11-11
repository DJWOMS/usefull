from django.db import models

from src.profiles.models import Profile
from src.team.models import Team


class Room(models.Model):
    name = models.CharField(max_length=50, default='')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rooms')
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='team_rooms',
        blank=True,
        null=True
    )
    member = models.ManyToManyField(Profile, related_name="room_members")
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ",\n".join([profile.username for profile in self.member.all()])


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    text = models.TextField(max_length=1024)
    create_date = models.DateTimeField(auto_now_add=True)
