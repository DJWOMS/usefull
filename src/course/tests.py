from django.contrib.auth.models import User
# Create your tests here.
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from src.course.models import Category, Course, Students, Lesson, Task, Comment, RealizationTask
from src.profiles.models import Profile


class CourseTest(APITestCase):
    def setUp(self):
        self.profile1 = Profile.objects.create(
            username='username1',
            phone='45675',
        )
        self.profile2 = Profile.objects.create(
            username='username2',
            phone='45675',
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
        self.comment1 = Comment.objects.create(
            user=self.profile1,
            lesson=self.lesson1,
            text='text1',
        )
        self.comment2 = Comment.objects.create(
            user=self.profile2,
            lesson=self.lesson1,
            text='text2',
        )
        self.student = Students.objects.create(user=self.profile1, course=self.course1)

        self.realization_task1 = RealizationTask.objects.create(
            task=self.task1,
            user=self.profile1,
            answer='dgdf',
            comment='dfgf',
            success=True
        )

    def test_category_list(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertTrue({'id': 1, 'name': 'category1'} in response.json())

    def test_course_list(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertTrue({'id': self.course1.id, 'name': 'course1', 'image': None, 'authors': [],
                         'lesson_count': 1, 'student_count': 1} in response.json())

    def test_course_detail(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('course_detail', kwargs={'pk': self.course1.id}))
        self.assertEqual(response.status_code, 200)

    def test_lesson_list_invalid(self):
        response = self.client.get(reverse('lesson_list', kwargs={'pk': self.course1.id}))
        self.assertEqual(response.status_code, 403)

    def test_lesson_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('lesson_list', kwargs={'pk': self.course1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertTrue({'id': self.lesson1.id, 'name': 'lesson1',
                         'image': None} in response.json())

    def test_lesson_detail_invalid(self):
        response = self.client.get(reverse('lesson_detail', kwargs={'pk': self.lesson1.id}))
        self.assertEqual(response.status_code, 403)

    def test_lesson_detail(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('lesson_detail', kwargs={'pk': self.lesson1.id}))
        self.assertEqual(response.status_code, 200)

    def test_task_list_invalid(self):
        response = self.client.get(reverse('task_list', kwargs={'pk': self.lesson1.id}))
        self.assertEqual(response.status_code, 403)

    def test_task_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('task_list', kwargs={'pk': self.lesson1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertTrue({'id': self.task2.id, 'title': 'task2',
                         'text': 'text2', 'realization_tasks': []} in response.json())

    def test_realization_task_create_invalid(self):
        response = self.client.post(reverse('realization_task_create'))
        self.assertEqual(response.status_code, 403)

    def test_realization_task_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'task': self.task1.id,
            'answer': 'hello',
            'comment': 'dfgfd'
        }
        response = self.client.post(reverse('realization_task_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_realization_task_detail_invalid(self):
        response = self.client.get(reverse('realization_task_detail',
                                           kwargs={'pk': self.realization_task1.id}))
        self.assertEqual(response.status_code, 403)

    def test_realization_task_detail(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('realization_task_detail',
                                           kwargs={'pk': self.realization_task1.id}))
        self.assertEqual(response.status_code, 200)

    def test_realization_task_update_invalid(self):
        response = self.client.put(reverse('realization_task_detail',
                                           kwargs={'pk': self.realization_task1.id}))
        self.assertEqual(response.status_code, 403)

    def test_realization_task_update_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile2)
        data = {
            'answer': 'hello',
            'comment': 'dfgfd'
        }
        response = self.client.put(reverse('realization_task_detail',
                                           kwargs={'pk': self.realization_task1.id}),
                                            data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_realization_task_update(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'task': self.task1.id,
            'answer': 'hello',
            'comment': 'dfgfd'
        }
        response = self.client.put(reverse('realization_task_detail',
                                           kwargs={'pk': self.realization_task1.id}),
                                            data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_realization_task_destroy_invalid(self):
        response = self.client.delete(reverse('realization_task_detail',
                                              kwargs={'pk': self.realization_task1.id}))
        self.assertEqual(response.status_code, 403)

    def test_realization_task_destroy_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile2)
        response = self.client.delete(reverse('realization_task_detail',
                                              kwargs={'pk': self.realization_task1.id}))
        self.assertEqual(response.status_code, 403)

    def test_realization_task_destroy(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('realization_task_detail',
                                              kwargs={'pk': self.realization_task1.id}))
        self.assertEqual(response.status_code, 204)

    def test_comment_list_invalid(self):
        response = self.client.get(reverse('comment_list', kwargs={'pk': self.lesson1.id}))
        self.assertEqual(response.status_code, 403)

    def test_comment_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('comment_list', kwargs={'pk': self.lesson1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_comment_create_invalid(self):
        response = self.client.post(reverse('comment_create'))
        self.assertEqual(response.status_code, 403)

    def test_comment_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'lesson': self.lesson1.id,
            'text': 'hello'
        }
        response = self.client.post(reverse('comment_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_comment_detail(self):
        response = self.client.get(reverse('comment_detail', kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, 200)

    def test_comment_update_invalid(self):
        response = self.client.put(reverse('comment_detail', kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, 403)

    def test_comment_update_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'lesson': self.lesson1.id,
            'text': 'goodbye'
        }
        response = self.client.put(reverse('comment_detail', kwargs={'pk': self.comment2.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_comment_update(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'lesson': self.lesson1.id,
            'text': 'goodbye'
        }
        response = self.client.put(reverse('comment_detail', kwargs={'pk': self.comment1.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_comment_destroy_invalid(self):
        response = self.client.delete(reverse('comment_detail', kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, 403)

    def test_comment_destroy_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('comment_detail', kwargs={'pk': self.comment2.id}))
        self.assertEqual(response.status_code, 403)

    def test_comment_destroy(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('comment_detail', kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, 204)

    def test_course_signup_invalid(self):
        response = self.client.post(reverse('course_signup'))
        self.assertEqual(response.status_code, 403)

    def test_course_signup(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'user': self.profile2.id,
            'course': self.course1.id
        }
        response = self.client.post(reverse('course_signup'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    # python manage.py test src
