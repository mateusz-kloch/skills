from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action

from django_articles.models import Article, Tag
from api.permissions import IsOwnerOrReadOnly
from api.serializers import ArticleSerializer, TagSerializer, UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(
            pub_date__lte=timezone.now()
        ).exclude(
            title=''
        ).exclude(
            tags__isnull=True
        ).exclude(
            content=''
        )
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
