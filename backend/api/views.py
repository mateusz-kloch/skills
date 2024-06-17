from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from .permissions import (
    ArticleIsOwnerOrReadOnly,
    AuthorIsSelfOrReadOnly,
    IsStaffOrReadOnly,
    IsAnonymousOrNotAllowed,
)
from .serializers import (
    AuthorSerializer,
    ArticleSerializer,
    TagSerializer,
)
from library.models import Article, Author, Tag


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Allows anyone to display published articles and
    to create a new article by logged in User.
    
    Uses custom permission `ArticleIsOwnerOrReadOnly` that allows only
    author of an article to edit it.
    """
    queryset = Article.verified_objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, ArticleIsOwnerOrReadOnly
    ]


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Allows anyone to display users and
    to create a new account by anonymous visitors.

    Uses custom permission `IsAnonymousOrNotAllowed` that allows only
    not logged in user to create an account.

    Uses custom permission `AuthorIsSelfOrReadOnly` that allows only
    a user to manage his personal data.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'slug'
    permission_classes = [IsAnonymousOrNotAllowed, AuthorIsSelfOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    """
    Allows anyone to display tags and articles related to them.
    
    Uses custom permission `IsStaffOrReadOnly` that allows only
    an staff user to manage tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    permission_classes = [IsStaffOrReadOnly]
