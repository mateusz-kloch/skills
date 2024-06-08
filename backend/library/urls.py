from django.urls import path, re_path
from django.views.generic import TemplateView

from .views import (
    ArticleListView,
    AuthorListView,
    AuthorDetailView,
    ArticleDetailView,
    TagListView,
    TagDetailView,
)


app_name = 'library'

urlpatterns = [
    path('', TemplateView.as_view(template_name='library/index.html'), name='index'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    re_path(r'^(?:article-(?P<pk>[0-9]+))/$', ArticleDetailView.as_view(), name='article-detail'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    re_path(r'^(?:author-(?P<pk>[0-9]+))/$', AuthorDetailView.as_view(), name='author-detail'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    re_path(r'^(?:tag-(?P<pk>[0-9]+))/$', TagDetailView.as_view(), name='tag-detail'),
]
