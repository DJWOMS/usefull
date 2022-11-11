from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from src.followers.models import Follower
from src.profiles.models import Profile


class FollowerTest(APITestCase):
    def setUp(self):
        self.profile1 = Profile.objects.create(
            username='username1',
            phone='45675',
        )
        self.profile2 = Profile.objects.create(
            username='username2',
            phone='68679t',
        )
        self.profile3 = Profile.objects.create(
            username='username3',
            phone='0773535',
        )
        self.follower1 = Follower.objects.create(
            user=self.profile1,
            subscriber=self.profile2
        )
        self.follower2 = Follower.objects.create(
            user=self.profile2,
            subscriber=self.profile1
        )
        self.follower3 = Follower.objects.create(
            user=self.profile2,
            subscriber=self.profile3
        )

    def test_follower_list_invalid(self):
        response = self.client.get(reverse('follower_list'))
        self.assertEqual(response.status_code, 403)

    def test_follower_list(self):
        self.client.force_authenticate(user=self.profile2)
        response = self.client.get(reverse('follower_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_follower_create_invalid(self):
        response = self.client.post(reverse('follower_detail'))
        self.assertEqual(response.status_code, 403)

    def test_follower_create(self):
        self.client.force_authenticate(user=self.profile2)
        data = {
            'following': self.profile3.id,
        }
        response = self.client.post(reverse('follower_detail'),
                                    data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_follower_destroy(self):
        self.client.force_authenticate(user=self.profile2)
        response = self.client.delete(reverse('following_delete', kwargs={'pk': self.profile1.id}))
        self.assertEqual(response.status_code, 204)

    # python manage.py test src
