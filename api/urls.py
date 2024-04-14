from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ArticleViewSet,
    CreateUserView,
    TagViewSet,
    UserViewSet
)


router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'register', CreateUserView, basename='user-register')

urlpatterns = [
    path('', include(router.urls)),
]
