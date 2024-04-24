from django.urls import path

from library.views import (
    AuthorIndexView,
    AuthorDetailView,
    ArticleIndexView,
    ArticleDetailView,
    TagIndexView,
    TagRelationsIndexView
)


app_name = 'library'

urlpatterns = [
    path('authors/', AuthorIndexView.as_view(), name='author-index'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('articles/', ArticleIndexView.as_view(), name='article-index'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('tags/', TagIndexView.as_view(), name='tag-index'),
    path('tags/<int:pk>/', TagRelationsIndexView.as_view(), name='tag-relations-index')
]
