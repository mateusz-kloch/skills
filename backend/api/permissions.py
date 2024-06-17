from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class ArticleIsOwnerOrReadOnly(permissions.BasePermission):
    """
    Ensures that only author of an Article object can manage it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author == request.user
        

class AuthorIsSelfOrReadOnly(permissions.BasePermission):
    """
    Ensures that only author himself can manage his data.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj == request.user
        

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Ensures that only staff user can create, edit or delete the object.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff
        

class IsAnonymousOrNotAllowed(permissions.BasePermission):
    """
    Ensures that only anonymous visitors can create a new account.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return isinstance(request.user, AnonymousUser)
        else:
            return True
