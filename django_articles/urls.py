from django.urls import path

from .views import (
    ArticlesIndexView,
    ArticlesDetailView,
    TagsIndexView,
    TagsRelationsIndexView
)


app_name = 'django_articles'

urlpatterns = [
    path('articles/', ArticlesIndexView.as_view(), name='articles_index'),
    path('articles/<int:pk>/', ArticlesDetailView.as_view(), name='articles_detail'),
    path('tags/', TagsIndexView.as_view(), name='tags_index'),
    path('tags/<int:pk>/', TagsRelationsIndexView.as_view(), name='tags_relations_index')
]