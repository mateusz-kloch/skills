from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action

from library.models import Article, Tag
from api.permissions import IsAnonOrNotAllowed ,IsOwnerOrReadOnly
from api.serializers import ArticleSerializer, TagSerializer, UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A set of views for Article model.

    Consists of Article list and detail views that allows anyone to display published articles and to create a new article by logged in User.
    
    Uses custom permission `IsOwnerOrReadOnly` that ensures only author of article can edit it.
    """
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
        """
        Assings User who create article as author of it.
        """
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Consists of Tag list and detail views that allows anyone to display tags and articles related to them.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Consists of User list and detail views that allows anyone to display users and create a new account by anonymous visitors.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, IsAnonOrNotAllowed]
