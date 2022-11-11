import os
from PIL import Image
from rest_framework.exceptions import ValidationError

from ...course.services import statistic_service


def delete_old_file(path_file):
    """ Удаление старого файла
    """
    if 'default/' not in path_file and os.path.exists(path_file):
        os.remove(path_file)


def validate_size_image(file_obj):
    """ Проверка размера файла
    """
    if file_obj:
        megabyte_limit = 1
        min_size = 90
        max_size = 720
        image = Image.open(file_obj)
        (width, height) = image.size
        if file_obj.size > megabyte_limit * 1024 * 1024:
            raise ValidationError(f"Максимальный размер файла {megabyte_limit}MB")
        elif width and height < min_size:
            raise ValidationError(f"Пожалуйста, загрузите картинку больше чем {min_size}x{min_size}.")
        elif width and height > max_size:
            raise ValidationError(f"Пожалуйста, загрузите картинку меньше чем {max_size}x{max_size}.")


class Progress:
    """Profile progress service"""

    def course_signup_count(self, user):
        return statistic_service.course_signup_count(user)

    def lesson_success_count(self, user):
        return statistic_service.lesson_success_count(user)

    def lesson_non_success_count(self, user):
        return statistic_service.lesson_non_success_count(user)

    def task_count(self, user):
        return statistic_service.task_count(user)

    def task_success_count(self, user):
        return statistic_service.task_success_count(user)


progress_service = Progress()
