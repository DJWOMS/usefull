import io
import tempfile

from PIL import Image
from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from src.course.models import Lesson, Category, Course, Task, Students, RealizationTask
from src.profiles.models import Profile


class ProfileTest(APITestCase):
    def setUp(self):
        self.profile1 = Profile.objects.create(
            username='username1',
            phone='45675',
            avatar=None
        )
        self.profile2 = Profile.objects.create(
            username='username2',
            phone='68679t',
        )
        self.profile3 = Profile.objects.create(
            username='username3',
            phone='0773535',
        )

        self.category = Category.objects.create(name='category1')

        self.course1 = Course.objects.create(
            category=self.category,
            name='course1',
            description='description1'
        )
        self.course2 = Course.objects.create(
            category=self.category,
            name='course2',
            description='description2',
            is_publish=False
        )
        self.lesson1 = Lesson.objects.create(
            course=self.course1,
            name='lesson1',
            text='text1',
        )
        self.lesson2 = Lesson.objects.create(
            course=self.course2,
            name='lesson1',
            text='text1',
        )
        self.task1 = Task.objects.create(
            lesson=self.lesson1,
            title='task1',
            text='text1',
        )
        self.task2 = Task.objects.create(
            lesson=self.lesson1,
            title='task2',
            text='text2',
        )
        self.task3 = Task.objects.create(
            lesson=self.lesson2,
            title='task3',
            text='text3',
        )

        self.student = Students.objects.create(user=self.profile1, course=self.course1)

        self.realization_task1 = RealizationTask.objects.create(
            task=self.task1,
            user=self.profile1,
            answer='dgdf',
            comment='dfgf',
            success=True
        )

        self.realization_task2 = RealizationTask.objects.create(
            task=self.task2,
            user=self.profile1,
            answer='dgdf',
            comment='dfgf',
            success=True
        )

    def test_profile_private_detail_invalid(self):
        response = self.client.get(reverse('profile_private_detail'))
        self.assertEqual(response.status_code, 403)

    def test_profile_private_detail(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('profile_private_detail'))
        self.assertEqual(response.status_code, 200)

    def test_profile_public_detail(self):
        response = self.client.get(reverse('profile_public_detail', kwargs={'pk': self.profile1.id}))
        self.assertEqual(response.status_code, 200)

    def test_progress(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('progress'))
        self.assertEqual(response.status_code, 200)

    # def test_avatar_update(self):
    #     self.client.force_authenticate(user=self.user1)
    #     avatar = Image.new('RGB', (100, 100))
    #     tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    #     avatar.save(tmp_file)
    #     # file = io.BytesIO()
    #     # image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    #     # image.save(file, 'png')
    #     # file.name = 'test.png'
    #     # file.seek(0)
    #     # response = self.client.put(reverse('update_avatar'),
    #     #                            {"avatar": avatar}, format='multipart')
    #     with open(tmp_file.name, 'rb') as data:
    #         response = self.client.put(reverse('update_avatar'),
    #                                    {"avatar": data}, format='multipart')
    #     print(response.json())
    #     self.assertEqual(response.status_code, 200)

    # python manage.py test src
