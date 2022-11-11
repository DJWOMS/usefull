from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from src.profiles.models import Profile
from src.support.models import Category, Ticket


class SupportTest(APITestCase):
    def setUp(self):
        self.profile1 = Profile.objects.create(
            username='username1',
            phone='45675',
            avatar=None
        )
        self.category1 = Category.objects.create(
            name='category1'
        )
        self.ticket1 = Ticket.objects.create(
            category=self.category1,
            user=self.profile1,
            title='title',
            text='text'
        )

    def test_ticket_list_invalid(self):
        response = self.client.post(reverse('ticket_list'))
        self.assertEqual(response.status_code, 403)

    def test_ticket_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertTrue({'id': self.ticket1.id, 'category': self.category1.name, 'title': 'title',
                         'status': 'open'} in response.json())

    def test_ticket_create_invalid(self):
        response = self.client.post(reverse('ticket_create'))
        self.assertEqual(response.status_code, 403)

    def test_ticket_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'category': self.category1.id,
            'title': 'fdgdg',
            'text': 'text'
        }
        response = self.client.post(reverse('ticket_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_category_list_invalid(self):
        response = self.client.get(reverse('support_category_list'))
        self.assertEqual(response.status_code, 403)

    def test_category_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('support_category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertTrue({'id': self.category1.id, 'name': 'category1'} in response.json())

    # python manage.py test src
