from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class ApiUserRegisterTests(APITestCase):
    def test_post_register_new_user(self):
        """
        Checks response for create new user.
        """
        user_data = {
            'username': 'author',
            'password': 'woeiuhtg9823y'
        }
        register = self.client.post('/api/register/', user_data)
        new_user = User.objects.get(username=user_data['username'])
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        self.assertQuerySetEqual(User.objects.all(), [new_user])


    def test_post_register_new_user_bad_password(self):
        """
        Checks response for create new user with poor password.
        """
        user_data = {
            'username': 'author',
            'password': 'password'
        }
        register = self.client.post('/api/register/', user_data)
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertQuerySetEqual(User.objects.all(), [])
