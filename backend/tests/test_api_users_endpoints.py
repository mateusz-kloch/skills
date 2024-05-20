from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from tests.utils import create_user, serialize_user_with_absolute_urls


class ApiUserListTests(APITestCase):
    def test_get_user_list_response(self):
        """
        Checks user list endpoint response.
        """
        serialized_first_user = serialize_user_with_absolute_urls(create_user('first_user', 'test123'))
        serialized_second_user = serialize_user_with_absolute_urls(create_user('second_user', 'test321'))
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'], [serialized_first_user, serialized_second_user])


    def test_get_user_list_response_no_users(self):
        """
        Checks user list endpoint response when there are no users in db.
        """
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])


    def test_post_user_list_new_user(self):
        """
        Checks user list endpoint response for create new user.
        """
        user_data = {
            'username': 'author',
            'password': 'woeiuhtg9823y'
        }
        register = self.client.post('/api/users/', user_data)
        new_user = User.objects.get(username=user_data['username'])
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        self.assertQuerySetEqual(User.objects.all(), [new_user])


    def test_post_user_list_new_user_bad_password(self):
        """
        Checks user list endpoint response for create new user with poor password.
        """
        user_data = {
            'username': 'author',
            'password': 'password'
        }
        register = self.client.post('/api/users/', user_data)
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertQuerySetEqual(User.objects.all(), [])

    
    def test_post_user_list_new_user_by_logged_user(self):
        """
        Checks user list endpoint respone for create new user if user is logged in.
        """
        user_data = {
            'username': 'user',
            'password': 'woeiuhtg9823y'
        }
        register = self.client.post('/api/users/', user_data)
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        self.client.login(username=user_data['username'], password=user_data['password'])
        new_user_data = {
            'username': 'new_user',
            'password': 'a82orsihg'
        }
        register = self.client.post('/api/users/', new_user_data)
        self.assertEqual(register.status_code, status.HTTP_403_FORBIDDEN)


class ApiUserDetailTests(APITestCase):
    def test_get_user_detail_response(self):
        """
        Checks user detail endpoint response for user in db.
        """
        serialized_user = serialize_user_with_absolute_urls(create_user('user', 'test123'))
        response = self.client.get(f'/api/users/{serialized_user["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_user)
