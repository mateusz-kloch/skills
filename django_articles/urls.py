from django.urls import path

from .views import (
    ArticleIndexView,
    ArticleDetailView,
    TagIndexView,
    TagRelationsIndexView
)


app_name = 'django_articles'

urlpatterns = [
    path('articles/', ArticleIndexView.as_view(), name='article_index'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('tags/', TagIndexView.as_view(), name='tag_index'),
    path('tags/<int:pk>/', TagRelationsIndexView.as_view(), name='tag_relations_index')
]
