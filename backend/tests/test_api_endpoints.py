"""
Tests for skills project api.

Tests are tagged with the name of the endpoint they concern.

Available tags:
- `api_root`
- `author_list_endpoint`
- `author_detail_endpoint`
- `tag_list_endpoint`
- `tag_detail_endpoint`
- `article_list_endpoint`
- `article_detail_endpoint`

Usage:
`python manage.py test --tag={tag_name}`
"""
from datetime import timedelta

from django.test import tag
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import Author
from library.models import Article, Tag
from common.test_utils import (
    create_article,
    create_author,
    create_tag,
    serialize_article,
    serialize_author,
    serialize_tag,
)


class ApiEndpointsTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.url_root = '/api/'
        self.url_article_list = '/api/articles/'
        self.url_author_list = '/api/authors/'
        self.url_tag_list = '/api/tags/'
        
        self.author = create_author('author', 'wao7984v')
        self.another_author = create_author('another_author', '28h4t032')

        self.staff_user = create_author('staff_user', '9aw4vt94hmt')
        self.staff_user.is_staff = True
        self.staff_user.save()
        
        self.tag = create_tag('tag')
        self.another_tag = create_tag('another_tag')
        
        self.past_article = create_article(
            title='past_article_title',
            author=self.author,
            tags=[self.tag],
            pub_date=timezone.now() - timedelta(hours=1),
            content='past_article_content',
        )
        self.future_article = create_article(
            title='future_article_title',
            author=self.author,
            tags=[self.tag],
            pub_date=timezone.now() + timedelta(hours=1),
            content='future_article_content',
        )
        self.new_article_data = {
            'title': 'new_article_title',
            'tags': [f'http://testserver/api/tags/{self.tag.id}/'],
            'pub_date': str(timezone.now() - timedelta(hours=1)),
            'content': 'new_article_content',
        }
        self.changed_article_data = {
            'title': 'changed_article_title',
            'tags': [f'http://testserver/api/tags/{self.another_tag.id}/'],
            'pub_date': str(timezone.now() - timedelta(hours=2)),
            'content': 'changed_article_content',
        }
        self.changed_article_title = {'title': 'changed_article_title'}

        self.new_author_data = {
            'user_name': 'new_author',
            'email': 'new_author@ex.com',
            'password': 'woeiuhtg9823y',
        }
        self.bad_author_data = {
            'user_name': 'author',
            'email': 'author@ex.com',
            'password': 'password',
        }

        self.new_tag_data = {'name': 'new_tag'}
        self.changed_tag_name = {'name': 'changed_tag_name'}

        self.serialized_author = serialize_author(self.author)
        self.serialized_another_author = serialize_author(self.another_author)
        self.serialized_staff_user = serialize_author(self.staff_user)
        
        self.serialized_tag = serialize_tag(self.tag)
        self.serialized_another_tag = serialize_tag(self.another_tag)
        
        self.serialized_past_article = serialize_article(self.past_article)
        self.serialized_future_article = serialize_article(self.future_article)


# Tests for API root:
    @tag('api_root')
    def test_get_api_root_response_status_code(self):
        """
        Checks API root response status code for unauthenticated user.
        """
        response = self.client.get(self.url_root)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Tests for Author list endpoint:
    @tag('author_list_endpoint')
    def test_get_author_list_response(self):
        """
        Checks author list endpoint response.
        """
        response = self.client.get(self.url_author_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [self.serialized_another_author, self.serialized_author, self.serialized_staff_user])

    @tag('author_list_endpoint')
    def test_get_author_list_response_no_authors(self):
        """
        Checks author list endpoint response when there are no authors in db.
        """
        Author.objects.all().delete()
        response = self.client.get(self.url_author_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    @tag('author_list_endpoint')
    def test_post_author_list_new_author(self):
        """
        Checks author list endpoint response for create new author.
        """
        register = self.client.post(self.url_author_list, self.new_author_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Author.objects.get(user_name=self.new_author_data['user_name']))

    @tag('author_list_endpoint')
    def test_post_author_list_new_author_bad_user_name(self):
        """
        Checks author list endpoint response for create new author with
        user_name that is already id database.
        """
        bad_author_data = {
            'user_name': self.bad_author_data['user_name'],
            'email': self.new_author_data['email'],
            'password': self.new_author_data['password'],
        }
        register = self.client.post(self.url_author_list, bad_author_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('author_list_endpoint')
    def test_post_author_list_new_author_bad_email(self):
        """
        Checks author list endpoint response for create new author with
        email that is already in database.
        """
        bad_author_data = {
            'user_name': self.new_author_data['user_name'],
            'email': self.bad_author_data['email'],
            'password': self.new_author_data['password'],
        }
        register = self.client.post(self.url_author_list, bad_author_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('author_list_endpoint')
    def test_post_author_list_new_author_bad_password(self):
        """
        Checks author list endpoint response for create new author with poor password.
        """
        bad_author_data = {
            'user_name': self.new_author_data['user_name'],
            'email': self.new_author_data['email'],
            'password': self.bad_author_data['password'],
        }
        register = self.client.post(self.url_author_list, bad_author_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('author_list_endpoint')
    def test_post_author_list_new_author_by_logged_author(self):
        """
        Checks author list endpoint respone for create new author if author is logged in.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        register = self.client.post(self.url_author_list, self.new_author_data)
        self.assertEqual(register.status_code, status.HTTP_403_FORBIDDEN)


# Tests for Author detail endpoint:
    @tag('author_detail_endpoint')
    def test_get_author_detail_response(self):
        """
        Checks author detail endpoint response for author in db.
        """
        response = self.client.get(f'{self.url_author_list}{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serialized_author)


# Tests for Tag list endpoint:
    @tag('tag_list_endpoint')
    def test_get_tag_list_response(self):
        """
        Checks tag list endpoint response when there are some tags in db.
        """
        response = self.client.get(self.url_tag_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [self.serialized_another_tag, self.serialized_tag])

    @tag('tag_list_endpoint')
    def test_get_tag_list_response_no_tags(self):
        """
        Checks tag list endpoint response when ther are no tags in db.
        """
        Tag.objects.all().delete()
        response = self.client.get(self.url_tag_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    @tag('tag_list_endpoint')
    def test_post_tag_list_new_tag_by_staff_user(self):
        """
        Checks tag list endpoint response for create a new tag object by
        staff user.
        """
        self.client.login(username=self.staff_user.user_name, password='9aw4vt94hmt')
        response = self.client.post(self.url_tag_list, self.new_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tag.objects.get(name=self.new_tag_data['name']))

    @tag('tag_list_endpoint')
    def test_post_tag_list_new_tag_by_not_staff_user(self):
        """
        Checks tag list endpoint response for create a new tag object by
        not staff user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.post(self.url_tag_list, self.new_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('tag_list_endpoint')
    def test_post_tag_list_new_tag_by_not_logged_user(self):
        """
        Checks tag list endpoint response for create a new tag object by
        not logged in user.
        """
        response = self.client.post(self.url_tag_list, self.new_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Tests for Tag detail endpoint:
    @tag('tag_detail_endpoint')
    def test_get_tag_detail_response_tag_exist(self):
        """
        Checks tag detail endpoint response for tag in db.
        """
        response = self.client.get(f'{self.url_tag_list}{self.tag.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serialized_tag)

    @tag('tag_detail_endpoint')
    def test_put_tag_detail_new_tag_by_staff_user(self):
        """
        Checks tag detail endpoint response for put a new data by staff user.
        """
        self.client.login(username=self.staff_user.user_name, password='9aw4vt94hmt')
        response = self.client.put(f'{self.url_tag_list}{self.tag.id}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.get(pk=self.tag.id).name, self.changed_tag_name['name'])

    @tag('tag_detail_endpoint')
    def test_put_tag_detail_new_tag_by_not_staff_user(self):
        """
        Checks tag detail endpoint response for put a new data by not staff user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.put(f'{self.url_tag_list}{self.tag.id}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('tag_detail_endpoint')
    def test_put_tag_detail_new_tag_by_not_logged_user(self):
        """
        Checks tag detail endpoint response for put a new data by not logged in user.
        """
        response = self.client.put(f'{self.url_tag_list}{self.tag.id}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('tag_detail_endpoint')
    def test_patch_tag_detail_new_tag_by_staff_user(self):
        """
        Checks tag detail endpoint response for update a tag data by staff user.
        """
        self.client.login(username=self.staff_user.user_name, password='9aw4vt94hmt')
        response = self.client.patch(f'{self.url_tag_list}{self.tag.id}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.get(pk=self.tag.id).name, self.changed_tag_name['name'])

    @tag('tag_detail_endpoint')
    def test_patch_tag_detail_new_tag_by_not_staff_user(self):
        """
        Checks tag detail endpoint response for update a tag data by not staff user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.patch(f'{self.url_tag_list}{self.tag.id}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('tag_detail_endpoint')
    def test_patch_tag_detail_new_tag_by_not_logged_user(self):
        """
        Checks tag detail endpoint response for update a tag data by not logged in user.
        """
        response = self.client.patch(f'{self.url_tag_list}{self.tag.id}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('tag_detail_endpoint')
    def test_delete_tag_detail_new_tag_by_staff_user(self):
        """
        Checks tag detail endpoint response for delete a tag object by
        staff user.
        """
        self.client.login(username=self.staff_user.user_name, password='9aw4vt94hmt')
        response = self.client.patch(f'{self.url_tag_list}{self.tag.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('tag_detail_endpoint')
    def test_delete_tag_detail_new_tag_by_not_staff_user(self):
        """
        Checks tag detail endpoint response for delete a tag object by
        not staff user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.patch(f'{self.url_tag_list}{self.tag.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('tag_detail_endpoint')
    def test_delete_tag_detail_new_tag_by_not_logged_user(self):
        """
        Checks tag detail endpoint response for delete a tag object by not logged in user.
        """
        response = self.client.patch(f'{self.url_tag_list}{self.tag.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Tests for Article list endpoint:
    @tag('article_list_endpoint')
    def test_get_article_list_response_no_articles(self):
        """
        Checks article list endpoint response when there are no articles in db.
        """
        Article.objects.all().delete()
        response = self.client.get(self.url_article_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    @tag('article_list_endpoint')
    def test_get_article_list_response_past_article(self):
        """
        Checks article list endpoint response when there is article with past pub_date in db.
        """
        response = self.client.get(self.url_article_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.serialized_past_article, response.data['results'])

    @tag('article_list_endpoint')
    def test_get_article_list_response_future_article(self):
        """
        Checks article list endpoint response when there is article with future pub_date in db.
        """
        response = self.client.get(self.url_article_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.serialized_future_article, response.data['results'])

    @tag('article_list_endpoint')
    def test_post_article_list_response_logged_user(self):
        """
        Checks article list endpoint response for create new article by logged user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.post(self.url_article_list, self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('article_list_endpoint')
    def test_post_article_list_response_not_logged_user(self):
        """
        Checks article list endpoint response for create new article by not logged user.
        """
        response = self.client.post(self.url_article_list, self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Tests for Article detail endpoint:
    @tag('article_detail_endpoint')
    def test_get_article_detail_response_past_article(self):
        """
        Checks article detail endpoint response for article with past pub_date. 
        """
        response = self.client.get(f'{self.url_article_list}{self.past_article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serialized_past_article)

    @tag('article_detail_endpoint')
    def test_get_article_detail_response_future_article(self):
        """
        Checks article detail endpoint response for article with future pub_date.
        """
        response = self.client.get(f'{self.url_article_list}{self.future_article.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag('article_detail_endpoint')
    def test_put_article_detail_logged_user_author(self):
        """
        Checks article detail endpoint response for new data added by logged user who is author of article.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.put(f'{self.url_article_list}{self.past_article.id}/', self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'new_article_title')

    @tag('article_detail_endpoint')
    def test_put_article_detail_logged_user_not_author(self):
        """
        Checks article detail endpoint response for new data added by logged user who is not author of article.
        """
        self.client.login(username=self.another_author, password='28h4t032')
        response = self.client.put(f'{self.url_article_list}{self.past_article.id}/', self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'past_article_title')

    @tag('article_detail_endpoint')
    def test_put_article_detail_not_logged_user(self):
        """
        Checks article detail endpoint response for new data added by not logged user.
        """
        response = self.client.put(f'{self.url_article_list}{self.past_article.id}/', self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'past_article_title')

    @tag('article_detail_endpoint')
    def test_patch_article_detail_logged_user_author(self):
        """
        Checks article detail endpoint response for new data updated by logged user who is author of article.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.patch(f'{self.url_article_list}{self.past_article.id}/', self.changed_article_title, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'changed_article_title')

    @tag('article_detail_endpoint')
    def test_patch_article_detail_logged_user_not_author(self):
        """
        Checks article detail endpoint response for new data updated by logged user who is not author of article.
        """
        self.client.login(username=self.another_author, password='28h4t032')
        response = self.client.patch(f'{self.url_article_list}{self.past_article.id}/', self.changed_article_title, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'past_article_title')

    @tag('article_detail_endpoint')
    def test_patch_article_detail_not_logged_user(self):
        """
        Checks article detail endpoint response for new data updated by not logged user.
        """
        response = self.client.patch(f'{self.url_article_list}{self.past_article.id}/', self.changed_article_title, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'past_article_title')

    @tag('article_detail_endpoint')
    def test_delete_article_detail_logged_user_author(self):
        """
        Checks article detail endpoint response for delete article by logged user who is author of article.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.delete(f'{self.url_article_list}{self.past_article.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.past_article, Article.objects.all())

    @tag('article_detail_endpoint')
    def test_delete_article_detail_logged_user_not_author(self):
        """
        Checks article detail endpoint response for delete article by logged user who is not author of article.
        """
        self.client.login(username=self.another_author, password='28h4t032')
        response = self.client.delete(f'{self.url_article_list}{self.past_article.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Article.objects.get(pk=self.past_article.id))

    @tag('article_detail_endpoint')
    def test_delete_article_detail_not_logged_user(self):
        """
        Checks article detail endpoint response for delete article by not logged user.
        """
        response = self.client.delete(f'{self.url_article_list}{self.past_article.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Article.objects.get(pk=self.past_article.id))
