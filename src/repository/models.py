from django.core.validators import FileExtensionValidator
from django.db import models
from src.profiles.models import Profile
from src.profiles.services.service import validate_size_image
from src.team.models import Team


class Category(models.Model):
    """ Categories by project """
    name = models.CharField(max_length=150)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name="children",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Toolkit(models.Model):
    """ Toolkit by project """
    name = models.CharField(max_length=150)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name="children",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    """ Model project """
    name = models.CharField(max_length=150)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    category = models.ForeignKey(
        Category,
        related_name="projects",
        on_delete=models.SET_NULL,
        null=True
    )
    toolkit = models.ManyToManyField(Toolkit, related_name="projects")
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    avatar = models.ImageField(
        upload_to='project/avatar/',
        default='/default/project.jpg',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image]
    )
    repository = models.CharField(max_length=150)
    star_count = models.PositiveIntegerField(blank=True, null=True)
    fork_count = models.PositiveIntegerField(blank=True, null=True)
    commit_count = models.PositiveIntegerField(blank=True, null=True)
    last_commit = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='project_members')
    project = models.ForeignKey(Project, related_name="members", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'User {} is member {} project'.format(self.user, self.project)
