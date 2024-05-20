from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from api.serializers import AuthorSerializer, ArticleSerializer, TagSerializer
from common.permissions import IsAnonymousOrNotAllowed ,IsOwnerOrReadOnly
from accounts.models import Author
from library.models import Article, Tag


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Allows anyone to display published articles and
    to create a new article by logged in User.
    
    Uses custom permission `IsOwnerOrReadOnly` that ensures only
    author of article is allowed to edit it.
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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Allows anyone to display tags and articles related to them.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AuthorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Allows anyone to display users and
    to create a new account by anonymous visitors.

    Uses custom permission `IsAnonymousOrNotAllowed` that ensures only
    not logged in user can create account.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAnonymousOrNotAllowed]
