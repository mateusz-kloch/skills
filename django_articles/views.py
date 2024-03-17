from django.utils import timezone
from django.views import generic

from .models import Article, Tag


class ArticlesIndexView(generic.ListView):
    template_name = 'django_articles/articles_index.html'
    context_object_name = 'published_articles_list'

    def get_queryset(self):
        return Article.objects.filter(date_published__lte=timezone.now())
    

class ArticlesDetailView(generic.DetailView):
    template_name = 'django_articles/articles_detail.html'

    def get_queryset(self):
        return Article.objects.filter(date_published__lte=timezone.now())


class TagsIndexView(generic.ListView):
    template_name = 'django_articles/tags_index.html'
    context_object_name = 'available_tags_list'

    def get_queryset(self):
        return Tag.objects.all()
    

class TagsRelationsIndexView(generic.ListView):
    template_name = 'django_articles/tags_relations_index.html'
    context_object_name = 'tags_relations_list'

    def get_queryset(self):
        search_request = self.request.resolver_match.kwargs.get('pk')
        return Article.objects.filter(tags__pk=search_request)
