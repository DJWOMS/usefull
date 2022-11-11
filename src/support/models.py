from django.db import models

from src.profiles.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS = (
        ('open', 'open'),
        ('closed', 'closed'),
        ('at_work', 'at_work')
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=1024)
    image = models.ImageField(upload_to='support/image/', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=7, choices=STATUS, default='open')

    def __str__(self):
        return self.title


class Faq(models.Model):
    """ Model for FAQ """
    question = models.CharField(max_length=150)
    answer = models.TextField()
    most = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class Guide(models.Model):
    """ Model for Guide """
    title = models.CharField(max_length=150)
    content = models.TextField()

    def __str__(self):
        return self.title
