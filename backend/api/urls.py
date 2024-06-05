from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ArticleViewSet,
    TagViewSet,
    AuthorViewSet,
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
