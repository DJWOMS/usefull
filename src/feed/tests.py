# from django.contrib.auth.models import User
# # Create your tests here.
# from django.urls import reverse
# from rest_framework.authtoken.models import Token
# from rest_framework.test import APITestCase
#
# from src.wall.models import Post
#
#
# class FeedTest(APITestCase):
#     def setUp(self):
#
#         self.user1 = User.objects.create(username="username1", password="sdgdsg431")
#         self.user_token1 = Token.objects.create(user=self.user1)
#
#         self.user2 = User.objects.create(username="username2", password="sdgdsg431")
#         self.user_token2 = Token.objects.create(user=self.user2)
#
#         self.post1 = Post.objects.create(
#             text='text1',
#             user=self.user1.id
#         )
#         self.post2 = Post.objects.create(
#             text='text2',
#             user=self.user2.id
#         )
#
#     def test_feed_invalid(self):
#         response = self.client.get(reverse('feed_list'))
#         self.assertEqual(response.status_code, 403)
#
#     def test_feed_list(self):
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.get(reverse('feed_list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 1)
#
#     def test_feed_detail(self):
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.get(reverse('feed_detail', kwargs={'pk': self.post2.id}))
#         self.assertEqual(response.status_code, 200)
#
#     def test_post_list(self):
#         response = self.client.get(reverse('post_list', kwargs={'pk': self.user1.id}))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 1)
#
#
#     # python manage.py test src
#
