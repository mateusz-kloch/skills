from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Author, Article, Tag


def create_author(name: str) -> Author:
    """
    Creates an Author model object.
    """
    return Author.objects.create(user_name=name, user_email=f'{name}@example.com')


def create_tag(name: str) -> Tag:
    """
    Creates a Tag model object.
    """
    return Tag.objects.create(name=name)


def create_article(title: str, author: Author, tags: list[Tag], pub_date: datetime, content: str) -> Article:
    """
    Creates an article model object and establishes a many-to-many relation with the given Tag objects.
    """
    article = Article(
        title=title,
        pub_date=pub_date,
        content=content
    )
    article.save()
    article.author = author
    article.tags.set(tags)
    return article


class AuthorModelTests(TestCase):
    def test_author_as_str(self):
        """
        Checks whether __str__() display tag correctly
        """
        author = create_author('test_author')
        self.assertIs(str(author), 'test_author')


class ArticleModelTests(TestCase):
    def test_article_as_str(self):
        """
        Checks whether __str__() displays article correctly.
        """
        title = 'test title'
        author = create_author('test_author')
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
        self.assertIs(str(article), 'test title')

    
    def test_article_tags_as_str_one_tag(self):
        """
        Checks whether tag_as_str() correctly displays tags if there is one tag.
        """
        title = 'test title'
        author = create_author('test_author')
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
        Checks whether tags_as_str() displays tags in aplhabetic order if there are multiple tags.
        """
        title = 'test title'
        author = create_author('test_author')
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
        Checks whether __str__() display tag correctly
        """
        tag = create_tag('test tag')
        self.assertIs(str(tag), 'test tag')


class AuthorIndexViewTests(TestCase):
    def test_no_authors(self):
        """
        Checks whether AuthorIndexView displays appropriate message when there are no authors.
        """
        response = self.client.get(reverse('django_articles:author_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No authors are available.')
        self.assertQuerySetEqual(
            response.context['authors_list'],
            []
        )


    def test_authors_alphabetic_order(self):
        """
        Checks whether AuthorIndexView displays authors in alphabetic order.
        """
        author_b = create_author('Author b')
        author_c = create_author('Author c')
        author_a = create_author('Author a')
        response = self.client.get(reverse('django_articles:author_index'))
        self.assertQuerySetEqual(
            response.context['authors_list'],
            [author_a, author_b, author_c]
        )


class AuthorDetailViewTests(TestCase):
    def test_past_article(self):
        """
        Checks whether AuthorDetailView displays related article with past pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now() - timedelta(days=1)
        content = 'test content'
        past_article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [past_article]
        )


    def test_present_article(self):
        """
        Checks whether AuthorDetailView displays related article with present pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now()
        content = 'test content'
        present_article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [present_article]
        )


    def test_future_article(self):
        """
        Checks whether AuthorDetailView not displays related article with future pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now() + timedelta(days=1)
        content = 'test content'
        create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertContains(response, 'Has not published any articles yet.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


    def test_past_and_present_article(self):
        """
        Checks whether AuthorDetailView displays related articles with past and present pub_dates.
        """
        past_title = 'past title'
        present_title = 'present title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        past_pub_date = timezone.now() - timedelta(days=1)
        present_pub_date = timezone.now()
        content = 'test content'
        past_article = create_article(
            title=past_title,
            author=author,
            tags=tags,
            pub_date=past_pub_date,
            content=content
        )
        present_article = create_article(
            title=present_title,
            author=author,
            tags=tags,
            pub_date=present_pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [past_article, present_article]
        )


    def test_past_and_future_article(self):
        """
        Checks whether AuthorDetailView displays related article with past pub_date but not article with future pub_date.
        """
        past_title = 'past title'
        future_title = 'future title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        past_pub_date = timezone.now() - timedelta(days=1)
        future_pub_date = timezone.now() + timedelta(days=1)
        content = 'test content'
        past_article = create_article(
            title=past_title,
            author=author,
            tags=tags,
            pub_date=past_pub_date,
            content=content
        )
        create_article(
            title=future_title,
            author=author,
            tags=tags,
            pub_date=future_pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [past_article]
        )


    def test_articles_alphabetic_order(self):
        """
        Checks whether AuthorDetailView displays related articles in alphabetical order of title.
        """
        title_c = 'title c'
        title_d = 'title d'
        title_b = 'title b'
        title_a = 'title a'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now()
        content = 'test content'
        article_c = create_article(
            title=title_c,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        article_d = create_article(
            title=title_d,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        article_b = create_article(
            title=title_b,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        article_a = create_article(
            title=title_a,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [article_a, article_b, article_c, article_d]
        )


    def test_article_with_missing_title_field(self):
        """
        Checks whether AuthorDetailView displays related article without title field.
        """
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.author = author
        article.tags.set([tag])
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertContains(response, 'Has not published any articles yet.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


    def test_article_with_missing_content_field(self):
        """
        Checks whether AuthorDetailView displays related article without content field.
        """
        title = 'test title'
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        article = Article(
            title=title,
            pub_date=pub_date
        )
        article.save()
        article.author = author
        article.tags.set([tag])
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertContains(response, 'Has not published any articles yet.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


    def test_article_without_related_tag(self):
        """
        Checks whether AuthorDetailView displays related article without relation with any Tag model object.
        """
        title = 'test title'
        author = create_author('test_author')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            title=title,
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.author = author
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


class ArticleIndexViewTests(TestCase):
    def test_no_articles(self):
        """
        Checks whether ArticleIndexView displays appropriate message when there are no articles.
        """
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )
    

    def test_past_article(self):
        """
        Checks whether ArticleIndexView displays article with past pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now() - timedelta(days=1)
        content = 'test content'
        past_article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [past_article]
        )


    def test_present_article(self):
        """
        Checks whether ArticleIndexView displays article with present pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now()
        content = 'test content'
        present_article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [present_article]
        )


    def test_future_article(self):
        """
        Checks whether ArticleIndexView not displays article with future pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now() + timedelta(days=1)
        content = 'test content'
        create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


    def test_past_and_present_article(self):
        """
        Checks whether ArticleIndexView displays articles with past and present pub_dates.
        """
        past_title = 'past title'
        present_title = 'present title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        past_pub_date = timezone.now() - timedelta(days=1)
        present_pub_date = timezone.now()
        content = 'test content'
        past_article = create_article(
            title=past_title,
            author=author,
            tags=tags,
            pub_date=past_pub_date,
            content=content
        )
        present_article = create_article(
            title=present_title,
            author=author,
            tags=tags,
            pub_date=present_pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [past_article, present_article]
        )


    def test_past_and_future_article(self):
        """
        Checks whether ArticleIndexView displays article with past pub_date but not article with future pub_date.
        """
        past_title = 'past title'
        future_title = 'future title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        past_pub_date = timezone.now() - timedelta(days=1)
        future_pub_date = timezone.now() + timedelta(days=1)
        content = 'test content'
        past_article = create_article(
            title=past_title,
            author=author,
            tags=tags,
            pub_date=past_pub_date,
            content=content
        )
        create_article(
            title=future_title,
            author=author,
            tags=tags,
            pub_date=future_pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [past_article]
        )


    def test_articles_alphabetic_order(self):
        """
        Checks whether ArticleIndexView displays articles in alphabetical order of title.
        """
        title_c = 'title c'
        title_d = 'title d'
        title_b = 'title b'
        title_a = 'title a'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now()
        content = 'test content'
        article_c = create_article(
            title=title_c,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        article_d = create_article(
            title=title_d,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        article_b = create_article(
            title=title_b,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        article_a = create_article(
            title=title_a,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [article_a, article_b, article_c, article_d]
        )


    def test_article_with_missing_title_field(self):
        """
        Checks whether ArticleIndexView displays article without title field.
        """
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.author = author
        article.tags.set([tag])
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


    def test_article_with_missing_content_field(self):
        """
        Checks whether ArticleIndexView displays article without content field.
        """
        title = 'test title'
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        article = Article(
            title=title,
            pub_date=pub_date
        )
        article.save()
        article.author = author
        article.tags.set([tag])
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


    def test_article_without_related_author(self):
        """
        Checks whether ArticleIndexView displays article without author.
        """
        title = 'test title'
        tags = [create_tag('test tag')]
        pub_date = timezone.now()
        content = 'test content'
        article = Article(title=title, pub_date=pub_date, content=content)
        article.save()
        article.tags.set(tags)
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [article]
        )


    def test_article_without_related_tag(self):
        """
        Checks whether ArticleIndexView displays article without relation with any Tag model object.
        """
        title = 'test title'
        author = create_author('test_author')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            title=title,
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.author = author
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


class ArticleDetailViewTests(TestCase):
    def test_published_article(self):
        """
        Checks whether ArticleDetailView displays article with past pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now() - timedelta(days=1)
        content = 'test content'
        past_article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_detail', args=[past_article.id]))
        self.assertContains(response, past_article.content)


    def test_not_yet_published_article(self):
        """
        Checks whether ArticleDetailView not displays article with future pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tags = [create_tag('test tag')]
        pub_date = timezone.now() + timedelta(days=1)
        content = 'test content'
        future_article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:article_detail', args=[future_article.id]))
        self.assertEqual(response.status_code, 404)


    def test_article_with_missing_title_field(self):
        """
        Checks whether ArticleDetailView displays article without title field.
        """
        author = create_author('test_author')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.author = author
        response = self.client.get(reverse('django_articles:article_detail', args=[article.id]))
        self.assertEqual(response.status_code, 404)


    def test_article_with_missing_content_field(self):
        """
        Checks whether ArticleDetailView displays article without content field.
        """
        title = 'test title'
        author = create_author('test_author')
        pub_date = timezone.now()
        article = Article(
            title=title,
            pub_date=pub_date
        )
        article.save()
        article.author = author
        response = self.client.get(reverse('django_articles:article_detail', args=[article.id]))
        self.assertEqual(response.status_code, 404)


    def test_article_without_related_tag(self):
        """
        Checks whether ArticleDetailView displays article without relation with any Tag model object.
        """
        title = 'test title'
        author = create_author('test_author')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            title=title,
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.author = author
        response = self.client.get(reverse('django_articles:article_detail', args=[article.id]))
        self.assertEqual(response.status_code, 404)


    def test_article_without_related_author(self):
        """
        Checks whether ArticleDetailView displays author of article as None when author field is not provided.
        """
        title = 'test title'
        tags = [create_tag('test tag')]
        pub_date = timezone.now()
        content = 'test content'
        article = Article(title=title, pub_date=pub_date, content=content)
        article.save()
        article.tags.set(tags)
        response = self.client.get(reverse('django_articles:article_detail', args=[article.id]))
        self.assertContains(response, None)


class TagIndexViewTests(TestCase):
    def test_no_tags(self):
        """
        Checks whether TagIndexView displays the appropriate message when there are no tags.
        """
        response = self.client.get(reverse('django_articles:tag_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No tags are available.')
        self.assertQuerySetEqual(
            response.context['available_tags_list'],
            []
        )


    def test_tags_alphabetic_order(self):
        """
        Checks whether TagIndexView displays tags in aplhabetic order.
        """
        tag_d = create_tag('tag d')
        tag_c = create_tag('tag c')
        tag_a = create_tag('tag a')
        tag_b = create_tag('tag b')
        response = self.client.get(reverse('django_articles:tag_index'))
        self.assertQuerySetEqual(
            response.context['available_tags_list'],
            [tag_a, tag_b, tag_c, tag_d]
        )


class TagRelationsIndexViewTests(TestCase):
    def test_no_articles(self):
        """
        Checks whether TagRelationsIndexView displays the appropriate message when there are no articles related with tag.
        """
        tag = create_tag('test tag')
        response = self.client.get(reverse('django_articles:tag_relations_index', args=[tag.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            []
        )


    def test_past_article(self):
        """
        Checks whether TagRelationsIndexView displays related article with past pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now() - timedelta(days=1)
        content = 'test content'
        past_article = create_article(
            title=title,
            author=author,
            tags=[tag],
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:tag_relations_index', args=[tag.id]))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [past_article]
        )


    def test_present_article(self):
        """
        Checks whether TagRelationsIndexView displays related article with present pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        content = 'test content'
        present_article = create_article(
            title=title,
            author=author,
            tags=[tag],
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:tag_relations_index', args=[tag.id]))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [present_article]
        )


    def test_future_article(self):
        """
        Checks whether TagRelationsIndexView not displays related article with future pub_date.
        """
        title = 'test title'
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now() + timedelta(days=1)
        content = 'test content'
        create_article(
            title=title,
            author=author,
            tags=[tag],
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:tag_relations_index', args=[tag.id]))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            []
        )


    def test_past_and_present_article(self):
        """
        Checks whether TagRelationsIndexView displays related articles with past and present pub_dates.
        """
        past_title = 'past title'
        present_title = 'present title'
        author = create_author('test_author')
        tag = create_tag('test tag')
        past_pub_date = timezone.now() - timedelta(days=1)
        present_pub_date = timezone.now()
        content = 'test content'
        past_article = create_article(
            title=past_title,
            author=author,
            tags=[tag],
            pub_date=past_pub_date,
            content=content
        )
        present_article = create_article(
            title=present_title,
            author=author,
            tags=[tag],
            pub_date=present_pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:tag_relations_index', args=[tag.id]))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [past_article, present_article]
        )


    def test_past_and_future_article(self):
        """
        Checks whether TagRelationsIndexView displays related article with past pub_date but not related article with future pub_date.
        """
        past_title = 'past title'
        future_title = 'future title'
        author = create_author('test_author')
        tag = create_tag('test tag')
        past_pub_date = timezone.now() - timedelta(days=1)
        future_pub_date = timezone.now() + timedelta(days=1)
        content = 'test content'
        past_article = create_article(
            title=past_title,
            author=author,
            tags=[tag],
            pub_date=past_pub_date,
            content=content
        )
        create_article(
            title=future_title,
            author=author,
            tags=[tag],
            pub_date=future_pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:tag_relations_index', args=[tag.id]))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [past_article]
        )


    def test_articles_alphabetic_order(self):
        """
        Checks whether TagRelationsIndexView displays related articles in alphabetical order of title.
        """
        title_c = 'title c'
        title_d = 'title d'
        title_b = 'title b'
        title_a = 'title a'
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        content = 'test content'
        article_c = create_article(
            title=title_c,
            author=author,
            tags=[tag],
            pub_date=pub_date,
            content=content
        )
        article_d = create_article(
            title=title_d,
            author=author,
            tags=[tag],
            pub_date=pub_date,
            content=content
        )
        article_b = create_article(
            title=title_b,
            author=author,
            tags=[tag],
            pub_date=pub_date,
            content=content
        )
        article_a = create_article(
            title=title_a,
            author=author,
            tags=[tag],
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('django_articles:tag_relations_index', args=[tag.id]))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [article_a, article_b, article_c, article_d]
        )


    def test_article_with_missing_title_field(self):
        """
        Checks whether TagRelationsIndexView displays article without title field.
        """
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.author = author
        article.tags.set([tag])
        response = self.client.get(reverse('django_articles:tag_relations_index', args=[tag.id]))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            []
        )


    def test_article_with_missing_content_field(self):
        """
        Checks whether TagRelationsIndexView displays article without content field.
        """
        title = 'test title'
        author = create_author('test_author')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        article = Article(
            title=title,
            pub_date=pub_date
        )
        article.save()
        article.author = author
        article.tags.set([tag])
        response = self.client.get(reverse('django_articles:tag_relations_index', args=[tag.id]))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            []
        )

    
    def test_article_without_related_author(self):
        """
        Checks whether TagRelationsIndexView displays article without author.
        """
        title = 'test title'
        tags = [create_tag('test tag')]
        pub_date = timezone.now()
        content = 'test content'
        article = Article(title=title, pub_date=pub_date, content=content)
        article.save()
        article.tags.set(tags)
        response = self.client.get(reverse('django_articles:article_index'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [article]
        )
