from django.views import generic

from .models import Article, Author, Tag


class ArticleListView(generic.ListView):
    template_name = 'library/article_list.html'
    context_object_name = 'published_articles_list'

    def get_queryset(self):
        """
        Returns a query set that includes verified articles
        whose pub_date is present or past.
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


class AuthorListView(generic.ListView):
    emplate_name = 'library/author_list.html'
    context_object_name = 'authors_list'

    def get_queryset(self):
        """
        Returns a query set that includes authors of published articles.
        """
        return Author.objects.all()
    

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'library/author_detail.html'

    def get_context_data(self, **kwargs):
        """
        Returns a queryset of articles related with an author,
        excludes defective articles.
        """
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        articles = Article.verified_objects.filter(author__pk=author.id)
        context['articles'] = articles
        return context


class TagListView(generic.ListView):
    template_name = 'library/tag_list.html'
    context_object_name = 'available_tags_list'

    def get_queryset(self):
        """
        Returns query set of all tags in database.
        """
        return Tag.objects.all()
    

class TagDetailView(generic.DetailView):
    model = Tag
    template_name = 'library/tag_detail.html'

    def get_context_data(self, **kwargs):
        """
        Returns a query set of verified articles whose
        tags contain the tag with primary key provided in the request.
        """
        context = super().get_context_data(**kwargs)
        search_request = self.request.resolver_match.kwargs.get('pk')
        articles = Article.verified_objects.filter(tags__pk=search_request)
        context['articles'] = articles
        return context
