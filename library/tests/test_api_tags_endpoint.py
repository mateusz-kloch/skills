from rest_framework import status
from rest_framework.test import APITestCase

from tests.utils import create_tag, serialize_tag_with_absolute_urls


class ApiTagListTest(APITestCase):
    def test_get_tag_list_response(self):
        """
        Checks tag-list response when there are some tags in db.
        """
        serialized_first_tag = serialize_tag_with_absolute_urls(create_tag('first_tag'))
        serialized_second_tag = serialize_tag_with_absolute_urls(create_tag('second_tag'))
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'], [serialized_first_tag, serialized_second_tag])


    def test_get_tag_list_response_no_tags(self):
        """
        Checks tag-list response when ther are no tags in db.
        """
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])


class ApiTagDetailTest(APITestCase):
    def test_tag_detail_response_tag_exist(self):
        """
        Checks tag-detail response for tag in db.
        """
        serialized_tag = serialize_tag_with_absolute_urls(create_tag('tag'))
        response = self.client.get(f'/api/tags/{serialized_tag["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_tag)
