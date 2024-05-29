from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from api.serializers import AuthorSerializer, ArticleSerializer, TagSerializer
from common.permissions import (
    IsStaffOrReadOnly, IsAnonymousOrNotAllowed ,IsOwnerOrReadOnly
)
from accounts.models import Author
from library.models import Article, Tag


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Allows anyone to display published articles and
    to create a new article by logged in User.
    
    Uses custom permission `IsOwnerOrReadOnly` that allows only
    author of an article to edit it.
    """
    queryset = Article.verified_objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        """
        Assings User who create article as author of it.
        """
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """
    Allows anyone to display tags and articles related to them.
    
    Uses custom permission `IsStaffOrReadOnly` that allows only
    an staff user to manage tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsStaffOrReadOnly]


class AuthorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Allows anyone to display users and
    to create a new account by anonymous visitors.

    Uses custom permission `IsAnonymousOrNotAllowed` that allows only
    not logged in user to create an account.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAnonymousOrNotAllowed]
