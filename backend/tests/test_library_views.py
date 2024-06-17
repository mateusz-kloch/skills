from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from common.test_utils import create_article, create_author, create_tag
from library.models import Article, Author, Tag


class SetUpData(TestCase):

    def setUp(self):
        self.index_template = 'library/index.html'
        self.article_list_template = 'library/article_list.html'
        self.article_detail_template = 'library/article_detail.html'
        self.author_list_template = 'library/author_list.html'
        self.author_detail_template = 'library/author_detail.html'
        self.tag_list_template = 'library/tag_list.html'
        self.tag_detail_template = 'library/tag_detail.html'
        self.user_register_template = 'library/user_register.html'
        self.user_login_template = 'library/user_login.html'
        self.user_logout_template = 'library/user_logout.html'
        
        self.index_url = 'library:index'
        self.article_list_url = 'library:article-list'
        self.article_detail_url = 'library:article-detail'
        self.author_list_url = 'library:author-list'
        self.author_detail_url = 'library:author-detail'
        self.tag_list_url = 'library:tag-list'
        self.tag_detail_url = 'library:tag-detail'
        self.user_register_url = 'library:user-register'
        self.user_login_url = 'library:user-login'
        self.user_logout_url = 'library:user-logout'
        
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

        self.user_login_data = {
            'user_name': 'author',
            'password': '48s5tb4w3'
        }


class IndexViewTests(SetUpData):

    def test_template_used(self):
        """
        Checks whether index page uses correct template.
        """
        response = self.client.get(reverse(self.index_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.index_template)


class ArticleListViewTests(SetUpData):

    def test_template_used(self):
        """
        Checks whether ArticleListView uses correct template.
        """
        response = self.client.get(reverse(self.article_list_url))
        self.assertTemplateUsed(response, self.article_list_template)

    def test_no_articles(self):
        """
        Checks whether ArticleListView displays appropriate message when there are no articles.
        """
        Article.objects.all().delete()
        response = self.client.get(reverse(self.article_list_url))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(response.context['published_articles_list'], [])
    
    def test_past_article(self):
        """
        Checks whether ArticleListView displays article with past pub_date.
        """
        response = self.client.get(reverse(self.article_list_url))
        self.assertQuerySetEqual(
            response.context['published_articles_list'], [self.past_article]
        )

    def test_future_article(self):
        """
        Checks whether ArticleListView not displays article with future pub_date.
        """
        response = self.client.get(reverse(self.article_list_url))
        self.assertNotIn(self.future_article, response.context['published_articles_list'])

    def test_article_with_missing_title_field(self):
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

    def test_article_with_missing_content_field(self):
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

    def test_article_without_related_tag(self):
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


class ArticleDetailViewTests(SetUpData):

    def test_template_used(self):
        """
        Checks whether ArticleDetailView uses correct template.
        """
        response = self.client.get(reverse(self.article_detail_url, args=(self.past_article.slug,)))
        self.assertTemplateUsed(response, self.article_detail_template)

    def test_past_article(self):
        """
        Checks whether ArticleDetailView displays article with past pub_date.
        """
        response = self.client.get(reverse(self.article_detail_url, args=(self.past_article.slug,)))
        self.assertContains(response, self.past_article)

    def test_future_published_article(self):
        """
        Checks whether ArticleDetailView not displays article with future pub_date.
        """
        response = self.client.get(reverse(self.article_detail_url, args=(self.future_article.slug,)))
        self.assertEqual(response.status_code, 404)

    def test_article_with_missing_title_field(self):
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

    def test_article_with_missing_content_field(self):
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

    def test_article_without_related_tag(self):
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


class AuthorListViewTests(SetUpData):

    def test_template_used(self):
        """
        Checks whether AuthorListView uses correct template.
        """
        response = self.client.get(reverse(self.author_list_url))
        self.assertTemplateUsed(response, self.author_list_template)
    
    def test_no_authors(self):
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


class AuthorDetailViewTests(SetUpData):

    def test_template_used(self):
        """
        Checks whether AuthorDetailView uses correct template.
        """
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertTemplateUsed(response, self.author_detail_template)

    def test_author_data(self):
        """
        Checks whether AuthorDetailView displays author data correctly.
        """
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertEqual(response.context['author'].user_name, self.author.user_name)
        self.assertEqual(response.context['author'].email, self.author.email)
        self.assertEqual(response.context['author'].joined, self.author.joined)

    def test_no_articles(self):
        """
        Checks whether AuthorDetailView displays appropriate message when there are
        no related articles with author.
        """
        Article.objects.all().delete()
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Has not published any articles yet.')
        self.assertQuerySetEqual(response.context['articles'], [])
    
    def test_past_article(self):
        """
        Checks whether AuthorDetailView displays related article with past pub_date.
        """
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertQuerySetEqual(
            response.context['articles'], [self.past_article]
        )

    def test_future_article(self):
        """
        Checks whether AuthorDetailView not displays related article with future pub_date.
        """
        response = self.client.get(reverse(self.author_detail_url, args=(self.author.slug,)))
        self.assertNotIn(self.future_article, response.context['articles'])

    def test_article_with_missing_title_field(self):
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

    def test_article_with_missing_content_field(self):
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

    def test_article_without_related_tag(self):
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


class TagListViewTests(SetUpData):

    def test_template_used(self):
        """
        Checks whether TagListView uses correct template.
        """
        response = self.client.get(reverse(self.tag_list_url))
        self.assertTemplateUsed(response, self.tag_list_template)

    def test_no_tags(self):
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


class TagDetailViewTests(SetUpData):

    def test_template_used(self):
        """
        Checks whether TagDetailView uses correct template.
        """
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertTemplateUsed(response, self.tag_detail_template)

    def test_tag_data(self):
        """
        Checks whether TagDetailView displays tag data correctly.
        """
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertEqual(response.context['tag'].name, self.tag.name)

    def test_no_articles(self):
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

    def test_past_article(self):
        """
        Checks whether TagDetailView displays related article with past pub_date.
        """
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertQuerySetEqual(
            response.context['articles'], [self.past_article]
        )

    def test_future_article(self):
        """
        Checks whether TagDetailView not displays related article with future pub_date.
        """
        response = self.client.get(reverse(self.tag_detail_url, args=(self.tag.slug,)))
        self.assertNotIn(self.future_article, response.context['articles'])

    def test_article_with_missing_title_field(self):
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

    def test_article_with_missing_content_field(self):
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


class UserRegisterViewTests(SetUpData):

    def test_templated_used(self):
        """
        Checks UserRegisterView templated used.
        """
        response = self.client.get(reverse(self.user_register_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.user_register_template)
    
    def test_new_user(self):
        """
        Checks whether UserRegisterView adds new user.
        """
        response = self.client.post(reverse(self.user_register_url), self.new_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Author.objects.get(user_name=self.new_user_data['user_name']))

    def test_already_logged_in_user(self):
        """
        Checks whether UserRegisterView redirects user that is already logged in.
        """
        login = self.client.login(username=self.author.user_name, password='48s5tb4w3')
        self.assertTrue(login)
        response = self.client.get(reverse(self.user_register_url))
        self.assertRedirects(response, reverse(self.index_url))


class UserLoginViewTests(SetUpData):

    def test_template_used(self):
        """
        Checks UserLoginView templated used.
        """
        response = self.client.get(reverse(self.user_login_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.user_login_template)

    def test_login(self):
        """
        Check whether UserLoginView logins users.
        """
        response = self.client.post(reverse(self.user_login_url), self.user_login_data)
        self.assertEqual(response.status_code, 200)

    def test_already_logged_in_user(self):
        """
        Checks whether UserLoginView redirects user that is already logged in.
        """
        login = self.client.login(username=self.author.user_name, password='48s5tb4w3')
        self.assertTrue(login)
        response = self.client.post(reverse(self.user_login_url), self.user_login_data)
        self.assertRedirects(response, reverse(self.index_url))

class UserLogoutViewTests(SetUpData):

    def test_templated_used(self):
        """
        Checks UserLogoutView templated used.
        """
        login = self.client.login(username=self.author.user_name, password='48s5tb4w3')
        self.assertTrue(login)
        response = self.client.post(reverse(self.user_logout_url))
        self.assertTemplateUsed(response, self.user_logout_template)

    def test_logout(self):
        """
        Checks whether UserLogoutView logouts users.
        """
        login = self.client.login(username=self.author.user_name, password='48s5tb4w3')
        self.assertTrue(login)
        response = self.client.post(reverse(self.user_logout_url))
        self.assertEqual(response.status_code, 200)


    def test_not_logged_in_user(self):
        """
        Checks whether UserLogoutView redirects user that is not logged in.
        """
        response = self.client.post(reverse(self.user_logout_url))
        self.assertRedirects(response, reverse(self.index_url))
