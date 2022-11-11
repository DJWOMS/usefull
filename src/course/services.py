from django.db.models import Count, Q

from src.course.models import Lesson, Task, Course


class Statistic:

    def course_signup_count(self, user):
        return Course.objects.filter(students__user=user.id).count()

    def lesson_success_count(self, user):
        return Lesson.objects.filter(course__students__user=user.id) \
            .annotate(success=Count('tasks', filter=Q(tasks__realization_tasks__success=True)),
                      realization_tasks=Count('tasks__realization_tasks'))\
            .filter(realization_tasks__gte=Count('tasks'), success__gte=Count('tasks')).count()

    def lesson_non_success_count(self, user):
        return Lesson.objects.filter(course__students__user=user.id) \
            .annotate(success=Count('tasks', filter=Q(tasks__realization_tasks__success=True)))\
            .filter(success__lt=Count('tasks')).count()

    def task_count(self, user):
        return Task.objects.filter(lesson__course__students__user=user.id).count()

    def task_success_count(self, user):
        return Task.objects.filter(realization_tasks__user=user.id,
                                   realization_tasks__success=True).count()


statistic_service = Statistic()
