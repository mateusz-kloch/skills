from rest_framework import status
from rest_framework.test import APITestCase


class ApiRootTests(APITestCase):
    def test_get_api_root_response_status_code(self):
        """
        Checks API root response status code.
        """
        url = '/api/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
