from django.urls import path, re_path
from django.views import generic

from . import views as library_views


app_name = 'library'

urlpatterns = [
    path(
        '', generic.TemplateView.as_view(
            template_name='library/index.html'
        ), name='index'
    ),
    path(
        'articles/', library_views.ArticleListView.as_view(), name='article-list'
    ),
    re_path(
        r'^(?:article-(?P<slug>[0-9-a-z]+))/$', library_views.ArticleDetailView.as_view(), name='article-detail'
    ),
    path(
        'authors/', library_views.AuthorListView.as_view(), name='author-list'
    ),
    re_path(
        r'^(?:author-(?P<slug>[0-9-a-z]+))/$', library_views.AuthorDetailView.as_view(), name='author-detail'
    ),
    path(
        'tags/', library_views.TagListView.as_view(), name='tag-list'
    ),
    re_path(
        r'^(?:tag-(?P<slug>[0-9-a-z]+))/$', library_views.TagDetailView.as_view(), name='tag-detail'
    ),
    path(
        'register/', library_views.UserRegisterView.as_view(), name='user-register'
    ),
    path(
        'login/', library_views.UserLoginView.as_view(), name='user-login'
    ),
    path(
        'logout/', library_views.UserLogoutView.as_view(), name='user-logout'
    ),
]
