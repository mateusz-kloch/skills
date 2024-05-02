from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Article
from library.tests.utils import create_article, create_tag, create_user, serialize_article_with_absolute_urls


class ApiArticleListTests(APITestCase):
    def test_get_article_list_response_no_articles(self):
        """
        Checks article list endpoint response when there are no articles in db.
        """
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])


    def test_get_article_list_response_past_article(self):
        """
        Checks article list endpoint response when there is article with past pub_date in db.
        """
        past_article = create_article(
            title='past_article_title',
            author=create_user('past_article_author', 'test123'),
            tags=[create_tag('past_article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='past_article_content',
        )
        serialized_past_article = serialize_article_with_absolute_urls(past_article)
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serialized_past_article, response.data['results'])


    def test_get_article_list_response_future_article(self):
        """
        Checks article list endpoint response when there is article with future pub_date in db.
        """
        future_article = create_article(
            title='future_article_title',
            author=create_user('future_article_author', 'test123'),
            tags=[create_tag('future_article_tag')],
            pub_date=timezone.now() + timedelta(hours=1),
            content='future_article_content',
        )
        serilized_future_article = serialize_article_with_absolute_urls(future_article)
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serilized_future_article, response.data['results'])


    def test_get_article_list_response_two_past_articles(self):
        """
        Checks article list endpoint response when there are two articles with past pub_date in db.
        """
        first_past_article = create_article(
            title='first_past_article_title',
            author=create_user('first_past_article_author', 'test123'),
            tags=[create_tag('first_past_article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='first_past_article_content'
        )
        second_past_article = create_article(
            title='second_past_article_title',
            author=create_user('second_past_article_author', 'test123'),
            tags=[create_tag('second_past_article_tag')],
            pub_date=timezone.now() - timedelta(hours=5),
            content='second_past_article_content'
        )
        serialized_first_past_article = serialize_article_with_absolute_urls(first_past_article)
        serialized_second_past_article = serialize_article_with_absolute_urls(second_past_article)
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serialized_first_past_article, response.data['results'])
        self.assertIn(serialized_second_past_article, response.data['results'])


    def test_get_article_list_response_past_and_future_article(self):
        """
        Checks article list endpoint response when there are article with past and article with future pub_date in db.
        """
        past_article = create_article(
            title='past_article_title',
            author=create_user('past_article_author', 'test123'),
            tags=[create_tag('past_article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='past_article_content'
        )
        future_article = create_article(
            title='future_article_title',
            author=create_user('future_article_author', 'test123'),
            tags=[create_tag('future_article_tag')],
            pub_date=timezone.now() + timedelta(hours=1),
            content='future_article_content'
        )
        serialized_past_article = serialize_article_with_absolute_urls(past_article)
        serialized_future_article = serialize_article_with_absolute_urls(future_article)
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serialized_past_article, response.data['results'])
        self.assertNotIn(serialized_future_article, response.data['results'])


    def test_post_article_list_response_logged_user(self):
        """
        Checks article list endpoint response for create new article by logged user.
        """
        create_user('user', 'test123')
        self.client.login(username='user', password='test123')
        article_data = {
            'title': 'article_title',
            'tags': [f"http://testserver/api/tags/{create_tag('tag').id}/"],
            'pub_date': str(timezone.now() - timedelta(hours=1)),
            'content': 'article_content'
        }
        response = self.client.post('/api/articles/', article_data, format='json')
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_article_list_response_logout_user(self):
        """
        Checks article list endpoint response for create new article after user is logged out.
        """
        create_user('user', 'test123')
        self.client.login(username='user', password='test123')
        self.client.logout()
        
        article_data = {
            'title': 'article_title',
            'tags': [f"http://testserver/api/tags/{create_tag('tag').id}/"],
            'pub_date': str(timezone.now() - timedelta(hours=1)),
            'content': 'article_content'
        }
        response = self.client.post('/api/articles/', article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_post_article_list_response_not_logged_user(self):
        """
        Checks article list endpoint response for create new article by not logged user.
        """
        article_data = {
            'title': 'article_title',
            'tags': ['tag'],
            'pub_date': str(timezone.now() - timedelta(hours=1)),
            'content': 'article_content'
        }
        response = self.client.post('/api/articles/', article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ApiArticleDetailTests(APITestCase):
    def test_get_article_detail_response_past_article(self):
        """
        Checks article detail endpoint response for article with past pub_date. 
        """
        past_article = create_article(
            title='past_article_title',
            author=create_user('past_article_author', 'test123'),
            tags=[create_tag('past_article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='past_article_content'
        )
        serialized_past_article = serialize_article_with_absolute_urls(past_article)
        response = self.client.get(f'/api/articles/{past_article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_past_article)


    def test_get_article_detail_response_future_article(self):
        """
        Checks article detail endpoint response for article with future pub_date.
        """
        future_article = create_article(
            title='future_article_title',
            author=create_user('future_article_author', 'test123'),
            tags=[create_tag('future_article_tag')],
            pub_date=timezone.now() + timedelta(hours=1),
            content='future_article_content'
        )
        response = self.client.get(f'/api/articles/{future_article.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_put_article_detail_logged_user_author(self):
        """
        Checks article detail endpoint response for new data added by logged user who is author of article.
        """
        user = create_user('author', 'test123')
        article = create_article(
            title='article_title',
            author=user,
            tags=[create_tag('article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='article_content'
        )
        new_data = {
            'title': 'new_article_title',
            'tags': [f"http://testserver/api/tags/{create_tag('new_tag').id}/"],
            'pub_date': str(timezone.now() - timedelta(hours=2)),
            'content': 'new_article_content'
        }
        self.client.login(username='author', password='test123')
        response = self.client.put(f'/api/articles/{article.id}/', new_data)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(Article.objects.all(), [article])
        self.assertEqual(Article.objects.get(pk=article.id).title, 'new_article_title')


    def test_put_article_detail_logged_user_not_author(self):
        """
        Checks article detail endpoint response for new data added by logged user who is not author of article.
        """
        article = create_article(
            title='article_title',
            author=create_user('article_author', 'test123'),
            tags=[create_tag('article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='article_content'
        )
        create_user('_not_author', 'test123')
        self.client.login(username='not_author', password='test123')
        new_data = {
            'title': 'new_article_title',
            'tags': [f"http://testserver/api/tags/{create_tag('new_tag').id}/"],
            'pub_date': str(timezone.now() - timedelta(hours=2)),
            'content': 'new_article_content'
        }
        response = self.client.put(f'/api/articles/{article.id}/', new_data)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=article.id).title, 'article_title')



    def test_put_article_detail_not_logged_user(self):
        """
        Checks article detail endpoint response for new data added by not logged user.
        """
        article = create_article(
            title='article_title',
            author=create_user('article_author', 'test123'),
            tags=[create_tag('article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='article_content'
        )
        new_data = {
            'title':'new_article_title',
            'tags': [f"http://testserver/api/tags/{create_tag('new_tag').id}/"],
            'pub_date': str(timezone.now() - timedelta(hours=2)),
            'content': 'new_article_content'
        }
        response = self.client.put(f'/api/articles/{article.id}/', new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=article.id).title, 'article_title')


    def test_patch_article_detail_logged_user_author(self):
        """
        Checks article detail endpoint response for new data updated by logged user who is author of article.
        """
        user = create_user('author', 'test123')
        article = create_article(
            title='article_title',
            author=user,
            tags=[create_tag('article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='article_content'
        )
        new_data = {'title': 'new_article_title',}
        self.client.login(username='author', password='test123')
        response = self.client.patch(f'/api/articles/{article.id}/', new_data)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerySetEqual(Article.objects.all(), [article])
        self.assertEqual(Article.objects.get(pk=article.id).title, 'new_article_title')


    def test_patch_article_detail_logged_user_not_author(self):
        """
        Checks article detail endpoint response for new data updated by logged user who is not author of article.
        """
        article = create_article(
            title='article_title',
            author=create_user('article_author', 'test123'),
            tags=[create_tag('article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='article_content'
        )
        create_user('_not_author', 'test123')
        self.client.login(username='not_author', password='test123')
        new_data = {'title': 'new_article_title',}
        response = self.client.patch(f'/api/articles/{article.id}/', new_data)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=article.id).title, 'article_title')



    def test_patch_article_detail_not_logged_user(self):
        """
        Checks article detail endpoint response for new data updated by not logged user.
        """
        article = create_article(
            title='article_title',
            author=create_user('article_author', 'test123'),
            tags=[create_tag('article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='article_content'
        )
        new_data = {'title':'new_article_title',}
        response = self.client.patch(f'/api/articles/{article.id}/', new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=article.id).title, 'article_title')


    def test_delete_article_detail_logged_user_author(self):
        """
        Checks article detail endpoint response for delete article by logged user who is author of article.
        """
        user = create_user('author', 'test123')
        article = create_article(
            title='article_title',
            author=user,
            tags=[create_tag('article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='article_content'
        )
        self.client.login(username='author', password='test123')
        response = self.client.delete(f'/api/articles/{article.id}/')
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertQuerySetEqual(Article.objects.all(), [])


    def test_delete_article_detail_logged_user_not_author(self):
        """
        Checks article detail endpoint response for delete article by logged user who is not author of article.
        """
        article = create_article(
            title='article_title',
            author=create_user('article_author', 'test123'),
            tags=[create_tag('article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='article_content'
        )
        create_user('not_author', 'test123')
        self.client.login(username='not_author', password='test123')
        response = self.client.delete(f'/api/articles/{article.id}/')
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=article.id).title, 'article_title')



    def test_delete_article_detail_not_logged_user(self):
        """
        Checks article detail endpoint response for delete article by not logged user.
        """
        article = create_article(
            title='article_title',
            author=create_user('article_author', 'test123'),
            tags=[create_tag('article_tag')],
            pub_date=timezone.now() - timedelta(hours=1),
            content='article_content'
        )
        response = self.client.delete(f'/api/articles/{article.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.get(pk=article.id).title, 'article_title')
