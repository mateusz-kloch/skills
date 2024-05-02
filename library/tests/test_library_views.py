from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from library.models import Article
from library.tests.utils import create_article, create_tag, create_user


class IndexPageTests(TestCase):
    def test_template_used(self):
        """
        Checks whether index page uses correct template.
        """
        expect_template = 'library/index.html'
        response = self.client.get(reverse('library:index'))
        self.assertTemplateUsed(response, expect_template)


class AuthorListViewTests(TestCase):
    def test_template_used(self):
        """
        Checks whether AuthorListView uses correct template.
        """
        expect_template = 'library/author_list.html'
        response = self.client.get(reverse('library:author-list'))
        self.assertTemplateUsed(response, expect_template)
    
    
    def test_no_authors(self):
        """
        Checks whether AuthorListView displays appropriate message when there are no authors.
        """
        response = self.client.get(reverse('library:author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No authors are available.')
        self.assertQuerySetEqual(
            response.context['authors_list'],
            []
        )


    def test_authors_alphabetic_order(self):
        """
        Checks whether AuthorListView displays authors in alphabetic order.
        """
        author_b = create_user('Author b', 'test123')
        author_c = create_user('Author c', 'test123')
        author_a = create_user('Author a', 'test123')
        response = self.client.get(reverse('library:author-list'))
        self.assertQuerySetEqual(
            response.context['authors_list'],
            [author_a, author_b, author_c]
        )


class AuthorDetailViewTests(TestCase):
    def test_template_used(self):
        """
        Checks whether AuthorDetailView uses correct template.
        """
        expect_template = 'library/author_detail.html'
        author = create_user('test_author', 'test123')
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertTemplateUsed(response, expect_template)


    def test_author_user_username(self):
        """
        Checks whether AuthorDetailView displays author related username.
        """
        author = create_user('test_author', 'test123')
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertContains(response, author.username)


    def test_author_user_email(self):
        """
        Checks whether AuthorDetailView displays author related email.
        """
        author = create_user('test_author', 'test123')
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertContains(response, author.email)


    def test_author_user_without_email(self):
        """
        Checks whether AuthorDetailView displays only username if related User not have email
        """
        author = User.objects.create_user(username='test_user', password='test123')
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertNotContains(response, 'E-mail:')


    def test_past_article(self):
        """
        Checks whether AuthorDetailView displays related article with past pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertQuerySetEqual(
            response.context['articles'],
            [past_article]
        )


    def test_present_article(self):
        """
        Checks whether AuthorDetailView displays related article with present pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertQuerySetEqual(
            response.context['articles'],
            [present_article]
        )


    def test_future_article(self):
        """
        Checks whether AuthorDetailView not displays related article with future pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertContains(response, 'Has not published any articles yet.')
        self.assertQuerySetEqual(
            response.context['articles'],
            []
        )


    def test_past_and_present_article(self):
        """
        Checks whether AuthorDetailView displays related articles with past and present pub_dates.
        """
        past_title = 'past title'
        present_title = 'present title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertQuerySetEqual(
            response.context['articles'],
            [present_article, past_article]
        )


    def test_past_and_future_article(self):
        """
        Checks whether AuthorDetailView displays related article with past pub_date but not article with future pub_date.
        """
        past_title = 'past title'
        future_title = 'future title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertQuerySetEqual(
            response.context['articles'],
            [past_article]
        )


    def test_articles_alphabetic_order(self):
        """
        Checks whether AuthorDetailView displays related articles ordered by date, latest first.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertQuerySetEqual(
            response.context['articles'],
            [article_a, article_b, article_c, article_d]
        )


    def test_article_with_missing_title_field(self):
        """
        Checks whether AuthorDetailView displays related article without title field.
        """
        author = create_user('test_author', 'test123')
        title = ''
        tag = create_tag('test tag')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            title=title,
            author=author,
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.tags.set([tag])
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertContains(response, 'Has not published any articles yet.')
        self.assertQuerySetEqual(
            response.context['articles'],
            []
        )


    def test_article_with_missing_content_field(self):
        """
        Checks whether AuthorDetailView displays related article without content field.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        article = Article(
            title=title,
            author=author,
            pub_date=pub_date
        )
        article.save()
        article.tags.set([tag])
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertContains(response, 'Has not published any articles yet.')
        self.assertQuerySetEqual(
            response.context['articles'],
            []
        )


    def test_article_without_related_tag(self):
        """
        Checks whether AuthorDetailView displays related article without relation with any Tag model object.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            title=title,
            author=author,
            pub_date=pub_date,
            content=content
        )
        article.save()
        response = self.client.get(reverse('library:author-detail', args=(author.id,)))
        self.assertContains(response, 'Has not published any articles yet.')
        self.assertQuerySetEqual(
            response.context['articles'],
            []
        )


class ArticleListViewTests(TestCase):
    def test_template_used(self):
        """
        Checks whether ArticleListView uses correct template.
        """
        expect_template = 'library/article_list.html'
        response = self.client.get(reverse('library:article-list'))
        self.assertTemplateUsed(response, expect_template)


    def test_no_articles(self):
        """
        Checks whether ArticleListView displays appropriate message when there are no articles.
        """
        response = self.client.get(reverse('library:article-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )
    

    def test_past_article(self):
        """
        Checks whether ArticleListView displays article with past pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:article-list'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [past_article]
        )


    def test_present_article(self):
        """
        Checks whether ArticleListView displays article with present pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:article-list'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [present_article]
        )


    def test_future_article(self):
        """
        Checks whether ArticleListView not displays article with future pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:article-list'))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


    def test_past_and_present_article(self):
        """
        Checks whether ArticleListView displays articles with past and present pub_dates.
        """
        past_title = 'past title'
        present_title = 'present title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:article-list'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [present_article, past_article]
        )


    def test_past_and_future_article(self):
        """
        Checks whether ArticleListView displays article with past pub_date but not article with future pub_date.
        """
        past_title = 'past title'
        future_title = 'future title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:article-list'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [past_article]
        )


    def test_articles_alphabetic_order(self):
        """
        Checks whether ArticleListView displays articles ordered by date, latest first.
        """
        title = 'test_title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:article-list'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            [article_a, article_b, article_c, article_d]
        )


    def test_article_with_missing_title_field(self):
        """
        Checks whether ArticleListView displays article without title field.
        """
        author = create_user('test_author', 'test123')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            author = author,
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.tags.set([tag])
        response = self.client.get(reverse('library:article-list'))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


    def test_article_with_missing_content_field(self):
        """
        Checks whether ArticleListView displays article without content field.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        article = Article(
            title=title,
            author = author,
            pub_date=pub_date
        )
        article.save()
        article.tags.set([tag])
        response = self.client.get(reverse('library:article-list'))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


    def test_article_without_related_tag(self):
        """
        Checks whether ArticleListView displays article without relation with any Tag model object.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            title=title,
            author = author,
            pub_date=pub_date,
            content=content
        )
        article.save()
        response = self.client.get(reverse('library:article-list'))
        self.assertQuerySetEqual(
            response.context['published_articles_list'],
            []
        )


class ArticleDetailViewTests(TestCase):
    def test_template_used(self):
        """
        Checks whether ArticleDetailView uses correct template.
        """
        expect_template = 'library/article_detail.html'
        title = 'test title'
        author = create_user('test_author', 'test123')
        tags = [create_tag('test tag')]
        pub_date = timezone.now() - timedelta(days=1)
        content = 'test content'
        article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('library:article-detail', args=(article.id,)))
        self.assertTemplateUsed(response, expect_template)


    def test_past_article(self):
        """
        Checks whether ArticleDetailView displays article with past pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:article-detail', args=(past_article.id,)))
        self.assertContains(response, past_article)


    def test_present_article(self):
        """
        Checks whether ArticleDetailView displays article with present pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
        tags = [create_tag('test tag')]
        pub_date = timezone.now() - timedelta(days=1)
        content = 'test content'
        present_article = create_article(
            title=title,
            author=author,
            tags=tags,
            pub_date=pub_date,
            content=content
        )
        response = self.client.get(reverse('library:article-detail', args=(present_article.id,)))
        self.assertContains(response, present_article)


    def test_future_published_article(self):
        """
        Checks whether ArticleDetailView not displays article with future pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:article-detail', args=(future_article.id,)))
        self.assertEqual(response.status_code, 404)


    def test_article_with_missing_title_field(self):
        """
        Checks whether ArticleDetailView displays article without title field.
        """
        author = create_user('test_author', 'test123')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            author = author,
            pub_date=pub_date,
            content=content
        )
        article.save()
        response = self.client.get(reverse('library:article-detail', args=(article.id,)))
        self.assertEqual(response.status_code, 404)


    def test_article_with_missing_content_field(self):
        """
        Checks whether ArticleDetailView displays article without content field.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
        pub_date = timezone.now()
        article = Article(
            title=title,
            author = author,
            pub_date=pub_date
        )
        article.save()
        response = self.client.get(reverse('library:article-detail', args=(article.id,)))
        self.assertEqual(response.status_code, 404)


    def test_article_without_related_tag(self):
        """
        Checks whether ArticleDetailView displays article without relation with any Tag model object.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            title=title,
            author = author,
            pub_date=pub_date,
            content=content
        )
        article.save()
        response = self.client.get(reverse('library:article-detail', args=(article.id,)))
        self.assertEqual(response.status_code, 404)


class TagListViewTests(TestCase):
    def test_template_used(self):
        """
        Checks whether TagListView uses correct template.
        """
        expect_template = 'library/tag_list.html'
        response = self.client.get(reverse('library:tag-list'))
        self.assertTemplateUsed(response, expect_template)


    def test_no_tags(self):
        """
        Checks whether TagListView displays the appropriate message when there are no tags.
        """
        response = self.client.get(reverse('library:tag-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No tags are available.')
        self.assertQuerySetEqual(
            response.context['available_tags_list'],
            []
        )


    def test_tags_alphabetic_order(self):
        """
        Checks whether TagListView displays tags in aplhabetic order.
        """
        tag_d = create_tag('tag d')
        tag_c = create_tag('tag c')
        tag_a = create_tag('tag a')
        tag_b = create_tag('tag b')
        response = self.client.get(reverse('library:tag-list'))
        self.assertQuerySetEqual(
            response.context['available_tags_list'],
            [tag_a, tag_b, tag_c, tag_d]
        )


class TagRelationsListViewTests(TestCase):
    def test_template_used(self):
        """
        Checks whether TagRelationsListView uses correct template.
        """
        expect_template = 'library/tag_relations_list.html'
        tag = create_tag('test tag')
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertTemplateUsed(response, expect_template)


    def test_no_articles(self):
        """
        Checks whether TagRelationsListView displays the appropriate message when there are no articles related with tag.
        """
        tag = create_tag('test tag')
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            []
        )


    def test_past_article(self):
        """
        Checks whether TagRelationsListView displays related article with past pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [past_article]
        )


    def test_present_article(self):
        """
        Checks whether TagRelationsListView displays related article with present pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [present_article]
        )


    def test_future_article(self):
        """
        Checks whether TagRelationsListView not displays related article with future pub_date.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            []
        )


    def test_past_and_present_article(self):
        """
        Checks whether TagRelationsListView displays related articles with past and present pub_dates.
        """
        past_title = 'past title'
        present_title = 'present title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [present_article, past_article]
        )


    def test_past_and_future_article(self):
        """
        Checks whether TagRelationsListView displays related article with past pub_date but not related article with future pub_date.
        """
        past_title = 'past title'
        future_title = 'future title'
        author = create_user('test_author', 'test123')
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
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [past_article]
        )


    def test_articles_alphabetic_order(self):
        """
        Checks whether TagRelationsListView displays related articles ordered by date, latest first.
        """
        title = 'test_title'
        author = create_user('test_author', 'test123')
        tag = create_tag('test tag')
        pub_date_a = timezone.now()
        pub_date_b = timezone.now() - timedelta(hours=1)
        pub_date_c = timezone.now() - timedelta(hours=2)
        pub_date_d = timezone.now() - timedelta(hours=3)
        content = 'test content'
        article_c = create_article(
            title=title,
            author=author,
            tags=[tag],
            pub_date=pub_date_c,
            content=content
        )
        article_d = create_article(
            title=title,
            author=author,
            tags=[tag],
            pub_date=pub_date_d,
            content=content
        )
        article_b = create_article(
            title=title,
            author=author,
            tags=[tag],
            pub_date=pub_date_b,
            content=content
        )
        article_a = create_article(
            title=title,
            author=author,
            tags=[tag],
            pub_date=pub_date_a,
            content=content
        )
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            [article_a, article_b, article_c, article_d]
        )


    def test_article_with_missing_title_field(self):
        """
        Checks whether TagRelationsListView displays article without title field.
        """
        author = create_user('test_author', 'test123')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        content = 'test content'
        article = Article(
            author = author,
            pub_date=pub_date,
            content=content
        )
        article.save()
        article.tags.set([tag])
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            []
        )


    def test_article_with_missing_content_field(self):
        """
        Checks whether TagRelationsListView displays article without content field.
        """
        title = 'test title'
        author = create_user('test_author', 'test123')
        tag = create_tag('test tag')
        pub_date = timezone.now()
        article = Article(
            title=title,
            author = author,
            pub_date=pub_date
        )
        article.save()
        article.tags.set([tag])
        response = self.client.get(reverse('library:tag-relations-list', args=(tag.id,)))
        self.assertContains(response, 'No articles are available.')
        self.assertQuerySetEqual(
            response.context['tag_relations_list'],
            []
        )
