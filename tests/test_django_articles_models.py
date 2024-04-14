from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from django_articles.models import Article, Tag
from tests.django_articles_test_utils import create_article, create_tag, create_user



class ArticleModelTests(TestCase):
    def test_article_as_str(self):
        """
        Checks whether __str__ displays article correctly.
        """
        title = 'test title'
        author = create_user('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now()
        content = 'test content'
        article = create_article(
            title=title,
            author = author,
            tags = tags,
            pub_date=pub_date,
            content=content
        )
        self.assertIs(str(article), article.title)


    def test_articles_ordering(self):
        """
        CHecks whether articles are ordered by pub_date, latest first.
        """
        title = 'test title'
        author = create_user('test_author')
        tags = [create_tag('test tag')]
        pub_date_a = timezone.now()
        pub_date_b = timezone.now() - timedelta(hours=1)
        pub_date_c = timezone.now() - timedelta(hours=2)
        pub_date_d = timezone.now() - timedelta(hours=3)
        content = 'test content'
        article_c = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date_c,
            content=content
        )
        article_d = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date_d,
            content=content
        )
        article_b = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date_b,
            content=content
        )
        article_a = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date_a,
            content=content
        )
        self.assertQuerySetEqual(
            Article.objects.all(),
            [article_a, article_b, article_c, article_d]
        )

    
    def test_article_tags_as_str_one_tag(self):
        """
        Checks whether tag_as_str() returns tag as string if ther is one related tag.
        """
        title = 'test title'
        author = create_user('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now()
        content = 'test content'
        article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        self.assertEqual(article.tags_as_str(), 'test tag')


    def test_articles_tags_as_str_many_tags(self):
        """
        Checks whether tags_as_str() returns tags as string in alphabetic order if there is many related tags.
        """
        title = 'test title'
        author = create_user('test_author')
        tags = [
            create_tag('tag b'),
            create_tag('tag d'),
            create_tag('tag c'),
            create_tag('tag a')
        ]
        pub_date = timezone.now()
        content = 'test content'
        article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        self.assertEqual(article.tags_as_str(), 'tag a, tag b, tag c, tag d')


class TagModelTests(TestCase):
    def test_tag_as_str(self):
        """
        Checks whether __str__ display tag correctly
        """
        tag = create_tag('test tag')
        self.assertIs(str(tag), tag.name)


    def test_tags_ordering(self):
        """
        Checks whether tags are ordered by name.
        """
        tag_b = create_tag('tag_b')
        tag_c = create_tag('tag_c')
        tag_a = create_tag('tag_a')
        self.assertQuerySetEqual(Tag.objects.all(), [tag_a, tag_b, tag_c])
