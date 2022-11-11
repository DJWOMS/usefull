from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from src.profiles.models import Profile
from src.wall.models import Post, Comment


class WallTest(APITestCase):
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
        self.post1 = Post.objects.create(
            text='text1',
            user=self.profile1
        )
        self.post2 = Post.objects.create(
            text='text2',
            user=self.profile2
        )
        self.comment1 = Comment.objects.create(
            user=self.profile1,
            post=self.post1,
            text='text1',
        )
        self.comment2 = Comment.objects.create(
            user=self.profile2,
            post=self.post1,
            text='text2',
        )

    def test_comment_create_invalid(self):
        response = self.client.post(reverse('wall_comment_create'))
        self.assertEqual(response.status_code, 403)

    def test_comment_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'post': self.post1.id,
            'text': 'hello'
        }
        response = self.client.post(reverse('wall_comment_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_comment_update_invalid(self):
        response = self.client.put(reverse('comment_detail', kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, 403)

    def test_comment_update_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'post': self.post1.id,
            'text': 'goodbye'
        }
        response = self.client.put(reverse('wall_comment_detail', kwargs={'pk': self.comment2.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_comment_update(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'post': self.post1.id,
            'text': 'goodbye'
        }
        response = self.client.put(reverse('wall_comment_detail', kwargs={'pk': self.comment1.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_comment_destroy_invalid(self):
        response = self.client.delete(reverse('wall_comment_detail',
                                              kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, 403)

    def test_comment_destroy_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('wall_comment_detail',
                                              kwargs={'pk': self.comment2.id}))
        self.assertEqual(response.status_code, 403)

    def test_comment_destroy(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(
            reverse('wall_comment_detail', kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, 204)

    def test_post_create_invalid(self):
        response = self.client.post(reverse('post_create'))
        self.assertEqual(response.status_code, 403)

    def test_post_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'text': 'text3'
        }
        response = self.client.post(reverse('post_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_detail(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_update_invalid(self):
        response = self.client.put(reverse('post_detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 403)

    def test_post_update_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'post': self.post1.id,
            'text': 'goodbye'
        }
        response = self.client.put(reverse('post_detail', kwargs={'pk': self.post2.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_update(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'post': self.post1.id,
            'text': 'goodbye'
        }
        response = self.client.put(reverse('post_detail', kwargs={'pk': self.post1.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_post_destroy_invalid(self):
        response = self.client.delete(reverse('post_detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 403)

    def test_post_destroy_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('post_detail', kwargs={'pk': self.post2.id}))
        self.assertEqual(response.status_code, 403)

    def test_post_destroy(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('post_detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 204)

    # python manage.py test src
