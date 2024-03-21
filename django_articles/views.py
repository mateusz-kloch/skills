from django.utils import timezone
from django.views import generic

from .models import Article, Tag


class ArticleIndexView(generic.ListView):
    template_name = 'django_articles/article_index.html'
    context_object_name = 'published_articles_list'

    def get_queryset(self):
        """
        Returns a query set that includes articles whose pub_data is present or past, and excludes articles with empty fields.
        """
        return Article.objects.filter(
            pub_date__lte=timezone.now()
        ).exclude(
            title=''
        ).exclude(
            tags__isnull=True
        ).exclude(
            content=''
        )
    

class ArticleDetailView(generic.DetailView):
    template_name = 'django_articles/article_detail.html'

    def get_queryset(self):
        """
        Returns a query set of the article whose primary key is provided in the request.
        """
        search_request = self.request.resolver_match.kwargs.get('pk')
        return Article.objects.filter(
            pk=search_request,
            pub_date__lte=timezone.now()
        ).exclude(
            tags__isnull=True
        )


class TagIndexView(generic.ListView):
    template_name = 'django_articles/tag_index.html'
    context_object_name = 'available_tags_list'

    def get_queryset(self):
        """
        Returns query set of all tags in database.
        """
        return Tag.objects.all()
    

class TagRelationsIndexView(generic.ListView):
    template_name = 'django_articles/tag_relations_index.html'
    context_object_name = 'tag_relations_list'

    def get_queryset(self):
        """
        Returns a query set of articles whose tags contain the tag with primary key provided in the request, and excludes articles with empty fields.
        """
        search_request = self.request.resolver_match.kwargs.get('pk')
        return Article.objects.filter(
            tags__pk=search_request,
            pub_date__lte=timezone.now()
        ).exclude(
                title=''
        ).exclude(
            content=''
        )
