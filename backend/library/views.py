from django.contrib.auth.models import User
from django.utils import timezone
from django.views import generic

from library.models import Article, Tag


class AuthorListView(generic.ListView):
    template_name = 'library/author_list.html'
    context_object_name = 'authors_list'

    def get_queryset(self):
        """
        Returns a query set that includes authors of published articles.
        """
        return User.objects.all().order_by('username')
    

class AuthorDetailView(generic.DetailView):
    model = User
    template_name = 'library/author_detail.html'

    def get_context_data(self, **kwargs):
        """
        Returns a queryset of articles related with an author, excludes defective articles.
        """
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        articles = Article.verified_objects.filter(author__pk=author.id)
        context['articles'] = articles
        return context


class ArticleListView(generic.ListView):
    template_name = 'library/article_list.html'
    context_object_name = 'published_articles_list'

    def get_queryset(self):
        """
        Returns a query set that includes verified articles whose pub_date is present or past.
        """
        return Article.verified_objects.all()
    

class ArticleDetailView(generic.DetailView):
    template_name = 'library/article_detail.html'

    def get_queryset(self):
        """
        Returns verified article whose primary key is provided in the request.
        """
        search_request = self.request.resolver_match.kwargs.get('pk')
        return Article.verified_objects.filter(pk=search_request)


class TagListView(generic.ListView):
    template_name = 'library/tag_list.html'
    context_object_name = 'available_tags_list'

    def get_queryset(self):
        """
        Returns query set of all tags in database.
        """
        return Tag.objects.all()
    

class TagRelationsListView(generic.ListView):
    template_name = 'library/tag_relations_list.html'
    context_object_name = 'tag_relations_list'

    def get_queryset(self):
        """
        Returns a query set of verified articles whose tags contain the tag with primary key provided in the request.
        """
        search_request = self.request.resolver_match.kwargs.get('pk')
        return Article.verified_objects.filter(tags__pk=search_request)
