from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ArticleViewSet,
    TagViewSet,
    UserViewSet
)


router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
