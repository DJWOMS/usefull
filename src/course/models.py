from django.db import models

from src.comments.models import AbstractComment
from src.profiles.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=150)
    is_publish = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Course(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='course/image/', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def lesson_count(self):
        return self.lessons.filter(course=self).count()

    def student_count(self):
        return self.students.filter(course=self).count()


class Author(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='authors'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='authors'
    )


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='lesson/image/', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    is_publish = models.BooleanField(default=True)
    text = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=150)
    text = models.TextField()
    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class RealizationTask(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='realization_tasks'
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='realization_tasks'

    )
    answer = models.TextField()
    comment = models.TextField()
    success = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)


class Students(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='students'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='students'
    )

    class Meta:
        verbose_name_plural = 'Students'


class Comment(AbstractComment):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='lesson_comments'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children')

    def __str__(self):
        return 'User {} commented lesson {}'.format(self.user, self.lesson)



