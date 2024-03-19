from django.utils import timezone
from django.views import generic

from .models import Article, Tag


class ArticleIndexView(generic.ListView):
    template_name = 'django_articles/article_index.html'
    context_object_name = 'published_articles_list'

    def get_queryset(self):
        return Article.objects.filter(
            tags__isnull=False,
            pub_date__lte=timezone.now()
        ).exclude(
            title=''
        ).exclude(
            content=''
        )
    

class ArticleDetailView(generic.DetailView):
    template_name = 'django_articles/article_detail.html'

    def get_queryset(self):
        return Article.objects.filter(
            tags__isnull=False,
            pub_date__lte=timezone.now()
        )


class TagIndexView(generic.ListView):
    template_name = 'django_articles/tag_index.html'
    context_object_name = 'available_tags_list'

    def get_queryset(self):
        return Tag.objects.all()
    

class TagRelationsIndexView(generic.ListView):
    template_name = 'django_articles/tag_relations_index.html'
    context_object_name = 'tag_relations_list'

    def get_queryset(self):
        search_request = self.request.resolver_match.kwargs.get('pk')
        return Article.objects.filter(
            tags__pk=search_request,
            pub_date__lte=timezone.now()
        ).exclude(
                title=''
        ).exclude(
            content=''
        )
