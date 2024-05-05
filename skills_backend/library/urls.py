from django.urls import path
from django.views.generic import TemplateView

from library.views import (
    AuthorListView,
    AuthorDetailView,
    ArticleListView,
    ArticleDetailView,
    TagListView,
    TagRelationsListView
)


app_name = 'library'

urlpatterns = [
    path('', TemplateView.as_view(template_name='library/index.html'), name='index'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagRelationsListView.as_view(), name='tag-relations-list')
]
