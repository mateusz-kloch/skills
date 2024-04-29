from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.test import APIClient


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Ensures that only author of an article can edit it.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author == request.user
        

class IsAnonymousOrNotAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Ensures that only anonymous visitors can create a new account.
        """
        if request.method in ['POST']:
            return isinstance(request.user, AnonymousUser)
        else:
            return True
