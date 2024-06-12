"""
Tests for `library` app views.

Tests are tagged with the name of the view they concern.

Available tags:
- `index_view`
- `article-list_view`
- `article-detail_view`
- `author-list_view`
- `author-detail_view`
- `tag-list_view`
- `tag-detail_view`

Usage:
`python manage.py test --tag={tag_name}`
"""
from datetime import timedelta

from django.test import tag, TestCase
from django.urls import reverse
from django.utils import timezone

from common.test_utils import create_article, create_author, create_tag
from library.models import Article, Author, Tag


class LibraryViewsTests(TestCase):

    def setUp(self):
        self.expect_index_template = 'library/index.html'
        self.expect_article_list_template = 'library/article_list.html'
        self.expect_article_detail_template = 'library/article_detail.html'
        self.expect_author_list_template = 'library/author_list.html'
        self.expect_author_detail_template = 'library/author_detail.html'
        self.expect_tag_list_template = 'library/tag_list.html'
        self.expect_tag_detail_template = 'library/tag_detail.html'
        
        self.index_url = ''
        self.article_list_url = 'library:article-list'
        self.article_detail_url = 'library:article-detail'
        self.author_list_url = 'library:author-list'
        self.author_detail_url = 'library:author-detail'
        self.tag_list_url = 'library:tag-list'
        self.tag_detail_url = 'library:tag-detail'
        self.user_register_url = 'library:user-register'
        
        self.author = create_author('author', '48s5tb4w3')

        self.tag = create_tag('test tag')

        self.past_article = create_article(
            title='past article title',
            author=self.author,
            tags=[self.tag],
            pub_date=timezone.now() - timedelta(days=1),
            content='past article content'
        )
        self.future_article = create_article(
            title='future article title',
            author=self.author,
            tags=[self.tag],
            pub_date=timezone.now() + timedelta(days=1),
            content='future article content'
        )

        self.new_user_data = {
            'user_name': 'newuser',
            'email': 'newuser@ex.com',
            'password': '4qa6gtv8o4',
            'password2': '4qa6gtv8o4'
        }

# Tests for index view:
    @tag('index_view')
    def test_template_used(self):
        """
        Checks whether index page uses correct template.
        """
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.expect_index_template)

# Tests for article-list view:
    @tag('article-list_view')
    def test_article_list_template_used(self):
        """
        Checks whether ArticleListView uses correct template.
        """
        response = self.client.get(reverse(self.article_list_url))
        self.assertTemplateUsed(response, self.expect_article_list_template)

    @tag('article-list_view')
    def test_article_list_no_articles(self):
        """
        Checks whether ArticleListView displays appropriate message when there are no articles.
        """
        Article.objects.all().delete()
        response = self.client.get(reverse(self.article_list_url))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(response.context['published_articles_list'], [])
    
    @tag('article-list_view')
    def test_article_list_past_article(self):
        """
        Checks whether ArticleListView displays article with past pub_date.
        """
        response = self.client.get(reverse(self.article_list_url))
        self.assertQuerySetEqual(
            response.context['published_articles_list'], [self.past_article]
        )

    @tag('article-list_view')
    def test_article_list_future_article(self):
        """
        Checks whether ArticleListView not displays article with future pub_date.
        """
        response = self.client.get(reverse(self.article_list_url))
        self.assertNotIn(self.future_article, response.context['published_articles_list'])

    @tag('article-list_view')
    def test_article_list_article_with_missing_title_field(self):
        """
        Checks whether ArticleListView not displays article without title field.
        """
        defective_article = Article(
            author=self.author,
            pub_date=timezone.now() - timedelta(hours=1),
            content='content'
        )
        defective_article.save()
        defective_article.tags.set([self.tag])
        response = self.client.get(reverse(self.article_list_url))
        self.assertNotIn(
            defective_article, response.context['published_articles_list']
        )

    @tag('article-list_view')
    def test_article_list_article_with_missing_content_field(self):
        """
        Checks whether ArticleListView not displays article without content field.
        """
        defective_article = Article(
            title='title',
            author = self.author,
            pub_date=timezone.now() - timedelta(hours=1),
        )
        defective_article.save()
        defective_article.tags.set([self.tag])
        response = self.client.get(reverse(self.article_list_url))
        self.assertNotIn(
            defective_article, response.context['published_articles_list']
        )

    @tag('article-list_view')
    def test_article_list_article_without_related_tag(self):
        """
        Checks whether ArticleListView not displays article without relation with any Tag model object.
        """
        defective_article = Article(
            title='title',
            author = self.author,
            pub_date=timezone.now() - timedelta(hours=1),
            content='content'
        )
        defective_article.save()
        response = self.client.get(reverse(self.article_list_url))
        self.assertNotIn(
            defective_article, response.context['published_articles_list']
        )

# Tests for article-detail view:
    @tag('article-detail_view')
    def test_article_detail_template_used(self):
        """
        Checks whether ArticleDetailView uses correct template.
        """
        response = self.client.get(reverse(self.article_detail_url, args=(self.past_article.slug,)))
        self.assertTemplateUsed(response, self.expect_article_detail_template)

    @tag('article-detail_view')
    def test_article_detail_past_article(self):
        """
        Checks whether ArticleDetailView displays article with past pub_date.
        """
        response = self.client.get(reverse(self.article_detail_url, args=(self.past_article.slug,)))
        self.assertContains(response, self.past_article)

    @tag('article-detail_view')
    def test_article_detail_future_published_article(self):
        """
        Checks whether ArticleDetailView not displays article with future pub_date.
        """
        response = self.client.get(reverse(self.article_detail_url, args=(self.future_article.slug,)))
        self.assertEqual(response.status_code, 404)

    @tag('article-detail_view')
    def test_article_detail_article_with_missing_title_field(self):
        """
        Checks whether ArticleDetailView displays article without title field.
        """
        defective_article = Article(
            slug='slug',
            author=self.author,
            pub_date=timezone.now() - timedelta(hours=1),
            content='content'
        )
        defective_article.save()
        defective_article.tags.set([self.tag])
        response = self.client.get(reverse(self.article_detail_url, args=(defective_article.slug,)))
        self.assertEqual(response.status_code, 404)

    @tag('article-detail_view')
    def test_article_detail_article_with_missing_content_field(self):
        """
        Checks whether ArticleDetailView displays article without content field.
        """
        defective_article = Article(
            title='title',
            author = self.author,
            pub_date=timezone.now() - timedelta(hours=1),
        )
        defective_article.save()
        defective_article.tags.set([self.tag])
        response = self.client.get(reverse(self.article_detail_url, args=(defective_article.slug,)))
        self.assertEqual(response.status_code, 404)

    @tag('article-detail_view')
    def test_article_detail_article_without_related_tag(self):
        """
        Checks whether ArticleDetailView displays article without relation with any Tag model object.
        """
        defective_article = Article(
            title='title',
            author = self.author,
            pub_date=timezone.now() - timedelta(hours=1),
            content='content'
        )
        defective_article.save()
        response = self.client.get(reverse(self.article_detail_url, args=(defective_article.slug,)))
        self.assertEqual(response.status_code, 404)

# Tests for author-list view:
    @tag('author-list_view')
    def test_author_list_template_used(self):
        """
        Checks whether AuthorListView uses correct template.
        """
        response = self.client.get(reverse(self.author_list_url))
        self.assertTemplateUsed(response, self.expect_author_list_template)
    
    @tag('author-list_view')
    def test_author_list_no_authors(self):
        """
        Checks whether AuthorListView displays appropriate message when there are no authors.
        """
        Author.objects.all().delete()
        response = self.client.get(reverse(self.author_list_url))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No authors are available.')
        self.assertQuerySetEqual(
            response.context['authors_list'],
            []
        )

# Tests for author-detail view:
    @tag('author-detail_view')
    def test_author_detail_template_used(self):
        """
        Checks whether AuthorDetailView uses correct template.
        """
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertTemplateUsed(response, self.expect_author_detail_template)

    @tag('author-detail_view')
    def test_author_detail_author_data(self):
        """
        Checks whether AuthorDetailView displays author data correctly.
        """
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertEqual(response.context['author'].user_name, self.author.user_name)
        self.assertEqual(response.context['author'].email, self.author.email)
        self.assertEqual(response.context['author'].joined, self.author.joined)

    @tag('author-detail_view')
    def test_author_detail_no_articles(self):
        """
        Checks whether AuthorDetailView displays appropriate message when there are
        no related articles with author.
        """
        Article.objects.all().delete()
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Has not published any articles yet.')
        self.assertQuerySetEqual(response.context['articles'], [])
    
    @tag('author-detail_view')
    def test_author_detail_past_article(self):
        """
        Checks whether AuthorDetailView displays related article with past pub_date.
        """
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertQuerySetEqual(
            response.context['articles'], [self.past_article]
        )

    @tag('author-detail_view')
    def test_author_detail_future_article(self):
        """
        Checks whether AuthorDetailView not displays related article with future pub_date.
        """
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertNotIn(self.future_article, response.context['articles'])

    @tag('author-detail_view')
    def test_author_detail_article_with_missing_title_field(self):
        """
        Checks whether AuthorDetailView not displays related article without title field.
        """
        defective_article = Article(
            author=self.author,
            pub_date=timezone.now() - timedelta(hours=1),
            content='content'
        )
        defective_article.save()
        defective_article.tags.set([self.tag])
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertNotIn(
            defective_article, response.context['articles']
        )

    @tag('author-detail_view')
    def test_author_detail_article_with_missing_content_field(self):
        """
        Checks whether AuthorDetailView not displays related article without content field.
        """
        defective_article = Article(
            title='title',
            author = self.author,
            pub_date=timezone.now() - timedelta(hours=1),
        )
        defective_article.save()
        defective_article.tags.set([self.tag])
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertNotIn(
            defective_article, response.context['articles']
        )

    @tag('author-detail_view')
    def test_author_detail_article_without_related_tag(self):
        """
        Checks whether AuthorDetailView not displays related article without
        relation with any Tag model object.
        """
        defective_article = Article(
            title='title',
            author = self.author,
            pub_date=timezone.now() - timedelta(hours=1),
            content='content'
        )
        defective_article.save()
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertNotIn(
            defective_article, response.context['articles']
        )

# Tests for tag-list view:
    @tag('tag-list_view')
    def test_tag_list_template_used(self):
        """
        Checks whether TagListView uses correct template.
        """
        response = self.client.get(reverse(self.tag_list_url))
        self.assertTemplateUsed(response, self.expect_tag_list_template)

    @tag('tag-list_view')
    def test_tag_list_no_tags(self):
        """
        Checks whether TagListView displays the appropriate message when there are no tags.
        """
        Tag.objects.all().delete()
        response = self.client.get(reverse(self.tag_list_url))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No tags are available.')
        self.assertQuerySetEqual(
            response.context['available_tags_list'], []
        )

# Tests for tag-detail view:
    @tag('tag-detail_view')
    def test_tag_detail_template_used(self):
        """
        Checks whether TagDetailView uses correct template.
        """
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertTemplateUsed(response, self.expect_tag_detail_template)

    @tag('tag-detail_view')
    def test_tag_detail_tag_data(self):
        """
        Checks whether TagDetailView displays tag data correctly.
        """
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertEqual(response.context['tag'].name, self.tag.name)

    @tag('tag-detail_view')
    def test_tag_detail_no_articles(self):
        """
        Checks whether TagDetailView displays the appropriate message when there are no articles related with tag.
        """
        Article.objects.all().delete()
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['articles'], []
        )

    @tag('tag-detail_view')
    def test_tag_detail_past_article(self):
        """
        Checks whether TagDetailView displays related article with past pub_date.
        """
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertQuerySetEqual(
            response.context['articles'], [self.past_article]
        )

    @tag('tag-detail_view')
    def test_tag_detail_future_article(self):
        """
        Checks whether TagDetailView not displays related article with future pub_date.
        """
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertNotIn(self.future_article, response.context['articles'])

    @tag('tag-detail_view')
    def test_tag_detail_article_with_missing_title_field(self):
        """
        Checks whether TagDetailView displays article without title field.
        """
        defective_article = Article(
            author=self.author,
            pub_date=timezone.now() - timedelta(hours=1),
            content='content'
        )
        defective_article.save()
        defective_article.tags.set([self.tag])
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertNotIn(defective_article, response.context['articles'])

    @tag('tag-detail_view')
    def test_tag_detail_article_with_missing_content_field(self):
        """
        Checks whether TagDetailView displays article without content field.
        """
        defective_article = Article(
            title='title',
            author = self.author,
            pub_date=timezone.now() - timedelta(hours=1),
        )
        defective_article.save()
        defective_article.tags.set([self.tag])
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertNotIn(defective_article, response.context['articles'])

# Tests for user-register view:
    @tag('user-register_view')
    def test_user_register_new_user(self):
        """
        Checks whether UserRegisterView adds new user.
        """
        response = self.client.post(reverse(self.user_register_url), self.new_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Author.objects.get(user_name=self.new_user_data['user_name']))
