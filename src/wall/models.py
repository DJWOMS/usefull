from django.db import models

from src.comments.models import AbstractComment
from src.profiles.models import Profile


class Post(models.Model):
    """ Post model"""
    VISIBILITY = (
        ('public', 'public'),
        ('private', 'private'),
        ('protected', 'protected')
    )
    text = models.TextField(max_length=1024)
    create_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    moderation = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='wall_posts'
    )
    visibility = models.CharField(max_length=30, choices=VISIBILITY, default='public')

    def __str__(self):
        # Post by {self.user} -
        return f'id {self.id}'

    def comments_count(self):
        return self.wall_comments.filter(is_delete=False).count()


class Comment(AbstractComment):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='wall_comments'
    )
    post = models.ForeignKey(
        Post,
        related_name="wall_comments",
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return 'User {} commented post {}'.format(self.user, self.post)
