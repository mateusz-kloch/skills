from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from library.models import Article, Author, Tag
from common.test_utils import (
    create_article,
    create_author,
    create_superuser,
    create_tag,
    serialize_article,
    serialize_author,
    serialize_tag,
)


class SetUpData(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.url_root = '/api/'
        self.url_article_list = '/api/articles/'
        self.url_author_list = '/api/authors/'
        self.url_tag_list = '/api/tags/'
        
        self.author = create_author('author', 'wao7984v')
        self.another_author = create_author('another_author', '28h4t032')

        self.superuser = create_superuser('superuser', '9aw4vt94hmt')
        
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
            'tags': [f'http://testserver/api/tags/{self.tag.slug}/'],
            'pub_date': str(timezone.now() - timedelta(hours=1)),
            'content': 'new_article_content',
        }
        self.changed_article_data = {
            'title': 'changed_article_title',
            'tags': [f'http://testserver/api/tags/{self.another_tag.slug}/'],
            'pub_date': str(timezone.now() - timedelta(hours=2)),
            'content': 'changed_article_content',
        }
        self.changed_article_title = {'title': 'changed_article_title'}

        self.new_author_data = {
            'user_name': 'new_author',
            'email': 'new_author@ex.com',
            'password': 'woeiuhtg9823y',
        }

        self.updated_author_data = {
            'user_name': 'new_user_name',
            'email': 'new_email@ex.com',
            'password': 'n3wpa55w0r0'
        }

        self.changed_author_username = {
            'user_name': 'changed_user_name'
        }
        
        self.repeatitive_user_name = 'author'
        self.repeatitive_email = 'author@ex.com'
        self.bad_email = 'not_an_email'
        self.bad_password = 'password'

        self.new_tag_data = {'name': 'new_tag'}
        self.changed_tag_name = {'name': 'changed_tag_name'}

        self.serialized_author = serialize_author(self.author)
        self.serialized_another_author = serialize_author(self.another_author)
        self.serialized_superuser = serialize_author(self.superuser)
        
        self.serialized_tag = serialize_tag(self.tag)
        self.serialized_another_tag = serialize_tag(self.another_tag)
        
        self.serialized_past_article = serialize_article(self.past_article)
        self.serialized_future_article = serialize_article(self.future_article)


class ApiRootTests(SetUpData):

    def test_get_response_status_code(self):
        """
        Checks API root response status code for unauthenticated user.
        """
        response = self.client.get(self.url_root)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorListEndpointTests(SetUpData):

    def test_get_response(self):
        """
        Checks author list endpoint response.
        """
        response = self.client.get(self.url_author_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [self.serialized_another_author, self.serialized_author, self.serialized_superuser])

    def test_get_response_no_authors(self):
        """
        Checks author list endpoint response when there are no authors in db.
        """
        Author.objects.all().delete()
        response = self.client.get(self.url_author_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_post_new_author(self):
        """
        Checks author list endpoint response for create new author.
        """
        register = self.client.post(self.url_author_list, self.new_author_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Author.objects.get(user_name=self.new_author_data['user_name']))

    def test_post_new_author_repeatitive_user_name(self):
        """
        Checks author list endpoint response for create new author with
        user_name that is already in database.
        """
        self.new_author_data['user_name'] = self.repeatitive_user_name
        register = self.client.post(self.url_author_list, self.new_author_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_new_author_repeatitive_email(self):
        """
        Checks author list endpoint response for create new author with
        email that is already in database.
        """
        self.new_author_data['email'] = self.repeatitive_email
        register = self.client.post(self.url_author_list, self.new_author_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_new_author_bad_email(self):
        """
        Checks author list endpoint response for create new author with bad email address.
        """
        self.new_author_data['email'] = self.bad_email
        register = self.client.post(self.url_author_list, self.new_author_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_new_author_bad_password(self):
        """
        Checks author list endpoint response for create new author with poor password.
        """
        self.new_author_data['password'] = self.bad_password
        register = self.client.post(self.url_author_list, self.new_author_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_new_author_by_logged_author(self):
        """
        Checks author list endpoint respone for create new author if author is logged in.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        register = self.client.post(self.url_author_list, self.new_author_data)
        self.assertEqual(register.status_code, status.HTTP_403_FORBIDDEN)


class AuthorDetailEndpointTests(SetUpData):

    def test_get_response(self):
        """
        Checks author detail endpoint response for author in db.
        """
        response = self.client.get(f'{self.url_author_list}{self.author.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serialized_author)

    def test_put_new_data_by_user_himself(self):
        """
        Checks auhtor detail endpoint response for put new data by himself.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.put(f'{self.url_author_list}{self.author.slug}/', self.new_author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.get(pk=self.author.id).user_name, self.new_author_data['user_name'])

    def test_put_new_data_by_other_user(self):
        """
        Checks auhtor detail endpoint response for put new data by not user himself.
        """
        self.client.login(username=self.another_author, password='28h4t032')
        response = self.client.put(f'{self.url_author_list}{self.author.slug}/', self.new_author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_new_data_by_anonymous_user(self):
        """
        Checks auhtor detail endpoint response for put new data by not logged in user.
        """
        response = self.client.put(f'{self.url_author_list}{self.author.slug}/', self.new_author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_data_by_user_himself(self):
        """
        Checks auhtor detail endpoint response for patch data by himself.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.patch(f'{self.url_author_list}{self.author.slug}/', self.changed_author_username, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.get(pk=self.author.id).user_name, self.changed_author_username['user_name'])

    def test_patch_data_by_other_user(self):
        """
        Checks auhtor detail endpoint response for patch data by not user himself.
        """
        self.client.login(username=self.another_author, password='28h4t032')
        response = self.client.patch(f'{self.url_author_list}{self.author.slug}/', self.changed_author_username, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_data_by_anonymous_user(self):
        """
        Checks auhtor detail endpoint response for patch data by not logged in user.
        """
        response = self.client.patch(f'{self.url_author_list}{self.author.slug}/', self.changed_author_username, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_data_by_user_himself(self):
        """
        Checks auhtor detail endpoint response for delete data by himself.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.delete(f'{self.url_author_list}{self.author.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.author, Author.objects.all())

    def test_delete_data_by_other_user(self):
        """
        Checks auhtor detail endpoint response for delete data by not user himself.
        """
        self.client.login(username=self.another_author, password='28h4t032')
        response = self.client.delete(f'{self.url_author_list}{self.author.slug}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_data_by_anonymous_user(self):
        """
        Checks auhtor detail endpoint response for delete data by not logged in user.
        """
        response = self.client.delete(f'{self.url_author_list}{self.author.slug}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TagListEndpointTests(SetUpData):

    def test_get_response(self):
        """
        Checks tag list endpoint response when there are some tags in db.
        """
        response = self.client.get(self.url_tag_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [self.serialized_another_tag, self.serialized_tag])

    def test_get_response_no_tags(self):
        """
        Checks tag list endpoint response when ther are no tags in db.
        """
        Tag.objects.all().delete()
        response = self.client.get(self.url_tag_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_post_new_tag_by_superuser(self):
        """
        Checks tag list endpoint response for create a new tag object by
        staff user.
        """
        self.client.login(username=self.superuser.user_name, password='9aw4vt94hmt')
        response = self.client.post(self.url_tag_list, self.new_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tag.objects.get(name=self.new_tag_data['name']))

    def test_post_new_tag_by_not_superuser(self):
        """
        Checks tag list endpoint response for create a new tag object by
        not staff user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.post(self.url_tag_list, self.new_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_new_tag_by_not_logged_user(self):
        """
        Checks tag list endpoint response for create a new tag object by
        not logged in user.
        """
        response = self.client.post(self.url_tag_list, self.new_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TagDetailEndpointTests(SetUpData):

    def test_get_response_tag_exist(self):
        """
        Checks tag detail endpoint response for tag in db.
        """
        response = self.client.get(f'{self.url_tag_list}{self.tag.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serialized_tag)

    def test_put_new_tag_by_superuser(self):
        """
        Checks tag detail endpoint response for put a new data by staff user.
        """
        self.client.login(username=self.superuser.user_name, password='9aw4vt94hmt')
        response = self.client.put(f'{self.url_tag_list}{self.tag.slug}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.get(pk=self.tag.id).name, self.changed_tag_name['name'])

    def test_put_new_tag_by_not_superuser(self):
        """
        Checks tag detail endpoint response for put a new data by not staff user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.put(f'{self.url_tag_list}{self.tag.slug}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_new_tag_by_not_logged_user(self):
        """
        Checks tag detail endpoint response for put a new data by not logged in user.
        """
        response = self.client.put(f'{self.url_tag_list}{self.tag.slug}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_new_tag_by_superuser(self):
        """
        Checks tag detail endpoint response for update a tag data by staff user.
        """
        self.client.login(username=self.superuser.user_name, password='9aw4vt94hmt')
        response = self.client.patch(f'{self.url_tag_list}{self.tag.slug}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.get(pk=self.tag.id).name, self.changed_tag_name['name'])

    def test_patch_new_tag_by_not_superuser(self):
        """
        Checks tag detail endpoint response for update a tag data by not staff user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.patch(f'{self.url_tag_list}{self.tag.slug}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_new_tag_by_not_logged_user(self):
        """
        Checks tag detail endpoint response for update a tag data by not logged in user.
        """
        response = self.client.patch(f'{self.url_tag_list}{self.tag.slug}/', self.changed_tag_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_new_tag_by_superuser(self):
        """
        Checks tag detail endpoint response for delete a tag object by
        staff user.
        """
        self.client.login(username=self.superuser.user_name, password='9aw4vt94hmt')
        response = self.client.patch(f'{self.url_tag_list}{self.tag.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_new_tag_by_not_superuser(self):
        """
        Checks tag detail endpoint response for delete a tag object by
        not staff user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.patch(f'{self.url_tag_list}{self.tag.slug}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_new_tag_by_not_logged_user(self):
        """
        Checks tag detail endpoint response for delete a tag object by not logged in user.
        """
        response = self.client.patch(f'{self.url_tag_list}{self.tag.slug}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ArticleListEndpointTests(SetUpData):

    def test_get_response_no_articles(self):
        """
        Checks article list endpoint response when there are no articles in db.
        """
        Article.objects.all().delete()
        response = self.client.get(self.url_article_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_get_response_past_article(self):
        """
        Checks article list endpoint response when there is article with past pub_date in db.
        """
        response = self.client.get(self.url_article_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.serialized_past_article, response.data['results'])

    def test_get_response_future_article(self):
        """
        Checks article list endpoint response when there is article with future pub_date in db.
        """
        response = self.client.get(self.url_article_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.serialized_future_article, response.data['results'])

    def test_post_response_logged_user(self):
        """
        Checks article list endpoint response for create new article by logged user.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.post(self.url_article_list, self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_response_not_logged_user(self):
        """
        Checks article list endpoint response for create new article by not logged user.
        """
        response = self.client.post(self.url_article_list, self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ArticleDetailEndpointTests(SetUpData):

    def test_get_response_past_article(self):
        """
        Checks article detail endpoint response for article with past pub_date. 
        """
        response = self.client.get(f'{self.url_article_list}{self.past_article.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.serialized_past_article)

    def test_get_response_future_article(self):
        """
        Checks article detail endpoint response for article with future pub_date.
        """
        response = self.client.get(f'{self.url_article_list}{self.future_article.slug}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_logged_user_author(self):
        """
        Checks article detail endpoint response for new data added by logged user who is author of article.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.put(f'{self.url_article_list}{self.past_article.slug}/', self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'new_article_title')

    def test_put_logged_user_not_author(self):
        """
        Checks article detail endpoint response for new data added by logged user who is not author of article.
        """
        self.client.login(username=self.another_author, password='28h4t032')
        response = self.client.put(f'{self.url_article_list}{self.past_article.slug}/', self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'past_article_title')

    def test_put_not_logged_user(self):
        """
        Checks article detail endpoint response for new data added by not logged user.
        """
        response = self.client.put(f'{self.url_article_list}{self.past_article.slug}/', self.new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'past_article_title')

    def test_patch_logged_user_author(self):
        """
        Checks article detail endpoint response for new data updated by logged user who is author of article.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.patch(f'{self.url_article_list}{self.past_article.slug}/', self.changed_article_title, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'changed_article_title')

    def test_patch_logged_user_not_author(self):
        """
        Checks article detail endpoint response for new data updated by logged user who is not author of article.
        """
        self.client.login(username=self.another_author, password='28h4t032')
        response = self.client.patch(f'{self.url_article_list}{self.past_article.slug}/', self.changed_article_title, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'past_article_title')

    def test_patch_not_logged_user(self):
        """
        Checks article detail endpoint response for new data updated by not logged user.
        """
        response = self.client.patch(f'{self.url_article_list}{self.past_article.slug}/', self.changed_article_title, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=self.past_article.id).title, 'past_article_title')

    def test_delete_logged_user_author(self):
        """
        Checks article detail endpoint response for delete article by logged user who is author of article.
        """
        self.client.login(username=self.author.user_name, password='wao7984v')
        response = self.client.delete(f'{self.url_article_list}{self.past_article.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.past_article, Article.objects.all())

    def test_delete_logged_user_not_author(self):
        """
        Checks article detail endpoint response for delete article by logged user who is not author of article.
        """
        self.client.login(username=self.another_author, password='28h4t032')
        response = self.client.delete(f'{self.url_article_list}{self.past_article.slug}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Article.objects.get(pk=self.past_article.id))

    def test_delete_not_logged_user(self):
        """
        Checks article detail endpoint response for delete article by not logged user.
        """
        response = self.client.delete(f'{self.url_article_list}{self.past_article.slug}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Article.objects.get(pk=self.past_article.id))
