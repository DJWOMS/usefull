from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from src.chat.models import Room, Message
from src.profiles.models import Profile


class ChatTest(APITestCase):
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

        self.room1 = Room.objects.create()
        self.room1.member.add(self.profile1, self.profile2)
        self.room1.save()

        self.message1 = Message.objects.create(
            user=self.profile1,
            room=self.room1,
            text='077dfgfh3535',
        )

    def test_room_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('room'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_room_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'member': self.profile3.id,
        }
        response = self.client.post(reverse('room'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_message_list_invalid_member(self):
        self.client.force_authenticate(user=self.profile3)
        response = self.client.get(reverse('message_list', kwargs={'pk': self.room1.id}))
        self.assertEqual(response.status_code, 403)

    def test_message_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('message_list', kwargs={'pk': self.room1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_message_create_invalid_member(self):
        self.client.force_authenticate(user=self.profile3)
        data = {
            'room': self.room1.id,
            'text': 'ghghjhg'
        }
        response = self.client.post(reverse('message_create'), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_message_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'room': self.room1.id,
            'text': 'ghghjhg'
        }
        response = self.client.post(reverse('message_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

        # python manage.py test src
