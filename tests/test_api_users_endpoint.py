from rest_framework import status
from rest_framework.test import APITestCase

from tests.utils import create_user, serialize_user_with_absolute_urls


class ApiUserListTests(APITestCase):
    def test_get_user_list_response(self):
        """
        Checks user-list response.
        """
        serialized_first_user = serialize_user_with_absolute_urls(create_user('first_user', 'test123'))
        serialized_second_user = serialize_user_with_absolute_urls(create_user('second_user', 'test321'))
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'], [serialized_first_user, serialized_second_user])


    def test_get_user_list_response_no_users(self):
        """
        Checks user-list response when there are no users in db.
        """
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])


class ApiUserDetailTests(APITestCase):
    def test_get_user_detail_response(self):
        """
        Checks user-detail response for user in db.
        """
        serialized_user = serialize_user_with_absolute_urls(create_user('user', 'test123'))
        response = self.client.get(f'/api/users/{serialized_user["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_user)
