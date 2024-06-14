from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views import generic

from .views import (
    ArticleDetailView,
    ArticleListView,
    AuthorDetailView,
    AuthorListView,
    TagDetailView,
    TagListView,
    UserRegisterView,
)


app_name = 'library'

urlpatterns = [
    path(
        '', generic.TemplateView.as_view(
            template_name='library/index.html'
        ), name='index'
    ),
    path(
        'articles/', ArticleListView.as_view(), name='article-list'
    ),
    re_path(
        r'^(?:article-(?P<slug>[0-9-a-z]+))/$', ArticleDetailView.as_view(), name='article-detail'
    ),
    path(
        'authors/', AuthorListView.as_view(), name='author-list'
    ),
    re_path(
        r'^(?:author-(?P<slug>[0-9-a-z]+))/$', AuthorDetailView.as_view(), name='author-detail'
    ),
    path(
        'tags/', TagListView.as_view(), name='tag-list'
    ),
    re_path(
        r'^(?:tag-(?P<slug>[0-9-a-z]+))/$', TagDetailView.as_view(), name='tag-detail'
    ),
    path(
        'register/', UserRegisterView.as_view(), name='user-register'
    ),
    path(
        'login/', auth_views.LoginView.as_view(
            template_name = 'library/user_login.html', next_page = 'library:index'
        ), name='user-login'
    ),
    path(
        'logout/', auth_views.LogoutView.as_view(
            template_name = 'library/user_logout.html'
        ), name='user-logout'
    ),
]
