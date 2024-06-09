"""
Tests for `library` app models.

Tests are tagged with the name of the model they concern.

Available tags:
- `article_model`
- `author_model`
- `tag_model`

Usage:
`python manage.py test --tag={tag_name}`
"""
from datetime import timedelta

from django.test import tag, TestCase
from django.utils import timezone

from library.models import Article, Author, Tag
from common.test_utils import create_article, create_author, create_tag


class LibraryModelsTests(TestCase):

    def setUp(self):
        self.author = create_author('author', '48s5tb4w3')
        self.another_author = create_author('another_author', 'a49o7wg3qvf')
        self.yet_another_author = create_author('yet_another_author', 'aiuh3h347q')

        self.tag = create_tag('tag')
        self.another_tag = create_tag('another_tag')
        self.yet_another_tag = create_tag('yet_another_tag')
        
        self.article = create_article(
            title='article title', 
            author=self.author,
            pub_date=timezone.now() - timedelta(hours=5),
            tags=[self.tag, self.another_tag],
            content='article content'
        )
        self.another_article = create_article(
            title='another article title',
            author=self.author,
            pub_date=timezone.now() - timedelta(hours=2),
            tags=[self.another_tag],
            content='another article content'
        )
        self.yet_another_article = create_article(
            title='yet another article title',
            author=self.author,
            pub_date=timezone.now(),
            tags=[self.yet_another_tag],
            content='yet another article content'
        )

# Tests for Author model:
    @tag('author_model')
    def test_author_str(self):
        """
        Checks whether __str__ displays author correctly.
        """
        self.assertEqual(self.author.user_name, str(self.author))

    @tag('author_model')
    def test_author_ordering(self):
        """
        CHecks whether authors are ordered by user_name.
        """
        self.assertQuerySetEqual(
            Author.objects.all(),
            [self.another_author, self.author, self.yet_another_author]
        )

    @tag('author_model')
    def test_author_default_joined(self):
        """
        Checks whether joined is provided by default.
        """
        self.assertTrue(self.author.joined)

    @tag('author_model')
    def test_author_default_slug(self):
        """
        Checks whether slug is provided by default.
        """
        self.assertTrue(self.author.slug)

    @tag('author_model')
    def test_author_default_avatar(self):
        """
        Checks whether default avatar is provided by default.
        """
        self.assertTrue(self.author.avatar)

# Tests for Tag model:
    @tag('tag_model')
    def test_tag_str(self):
        """
        Checks whether __str__ displays tag correctly.
        """
        self.assertEqual(self.tag.name, str(self.tag))

    @tag('tag_model')
    def test_tag_ordering(self):
        """
        CHecks whether tags are ordered by name.
        """
        self.assertQuerySetEqual(
            Tag.objects.all(),
            [self.another_tag, self.tag, self.yet_another_tag]
        )

    @tag('tag_model')
    def test_tag_default_slug(self):
        """
        Checks whether slug is provided by default.
        """
        self.assertTrue(self.tag.slug)

# Tests for Article model:
    @tag('article_model')
    def test_article_str(self):
        """
        Checks whether __str__ displays article correctly.
        """
        self.assertEqual(self.article.title, str(self.article))

    @tag('article_model')
    def test_article_ordering(self):
        """
        CHecks whether tags are ordered by pub_date, latest first.
        """
        self.assertQuerySetEqual(
            Article.objects.all(),
            [self.yet_another_article, self.another_article, self.article]
        )

    @tag('article_model')
    def test_article_default_pub_date(self):
        """
        Checks whether pub_date is provided by default.
        """
        test_article = Article(
            title='title',author=self.author, content='content'
        )
        test_article.save()
        test_article.tags.set([self.tag])
        self.assertTrue(self.article.pub_date)

    @tag('article_model')
    def test_article_default_slug(self):
        """
        Checks whether slug is provided by default.
        """
        self.assertTrue(self.article.slug)

    @tag('article_model')
    def test_article_tags_as_str(self):
        """
        Checks whether tag_as_str() correctly returns tags as string.
        """
        self.assertEqual(self.article.tags_as_str(), 'another_tag, tag')
