"""
Tests for utilities that are used in tests modules.
"""
from django.test import TestCase
from django.utils import timezone

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


class UtilsTests(TestCase):

    def setUp(self):
        self.test_author = create_author(
            user_name='test_author', password='s874v5t3w'
        )
        self.test_tag = create_tag(
            name='test_tag'
        )
        self.date = timezone.now()
        self.test_article = create_article(
            title='test_title',
            author=self.test_author,
            pub_date=self.date,
            tags=[self.test_tag],
            content='test_content'
        )
        self.serialized_test_author = serialize_author(self.test_author)
        self.serialized_test_tag = serialize_tag(self.test_tag)
        self.serialized_test_article = serialize_article(self.test_article)

    def test_create_author(self):
        """
        Checks whether the create_author function creates Author model object,
        sets attributes correctly and
        that the author created using it can log in.
        """
        login = self.client.login(username='test_author', password='s874v5t3w')
        self.assertTrue(login)
        self.assertEqual(self.test_author.user_name, 'test_author')
        self.assertEqual(self.test_author.email, 'test_author@ex.com')
        self.assertTrue(self.test_author.password)
        self.assertTrue(self.test_author.is_active)
        self.assertTrue(Author.objects.get(user_name='test_author'))

    def test_create_tag(self):
        """
        Checks whether the create_tag function creates Tag model object and
        sets attributes correctly.
        """
        self.assertEqual(self.test_tag.name, 'test_tag')
        self.assertTrue(Tag.objects.get(name='test_tag'))

    def test_create_article(self):
        """
        Checks whether the create_article function creates Article model object and
        sets attributes correctly.
        """
        self.assertEqual(self.test_article.title, 'test_title')
        self.assertEqual(self.test_article.author, self.test_author)
        self.assertEqual(self.test_article.pub_date, self.date)
        self.assertQuerySetEqual(self.test_article.tags.all(), [self.test_tag])
        self.assertEqual(self.test_article.content, 'test_content')
        self.assertTrue(Article.objects.get(title='test_title'))

    def test_serialize_author(self):
        """
        Checks whether serialize_author function propertly adds absolute urls.
        """
        expect = {
            'url': 'http://testserver/api/authors/1/',
            'articles': ['http://testserver/api/articles/1/'],
        }
        self.assertEqual(self.serialized_test_author['url'], expect['url'])
        self.assertEqual(self.serialized_test_author['articles'], expect['articles'])

    def test_serialize_tag(self):
        """
        Checks whether serialize_tag function propertly adds absolute urls.
        """
        expect = {
            'url': 'http://testserver/api/tags/1/',
            'articles' : ['http://testserver/api/articles/1/'],
        }
        self.assertEqual(self.serialized_test_tag['url'], expect['url'])
        self.assertEqual(self.serialized_test_tag['articles'], expect['articles'])

    def test_serialize_article(self):
        """
        Checks whether serialize_article function propertly adds absolute urls.
        """
        expect = {
            'url': 'http://testserver/api/articles/1/',
            'author': 'http://testserver/api/authors/1/',
            'tags': ['http://testserver/api/tags/1/'],

        }
        self.assertEqual(self.serialized_test_article['url'], expect['url'])
        self.assertEqual(self.serialized_test_article['author'], expect['author'])
        self.assertEqual(self.serialized_test_article['tags'],expect['tags'])
