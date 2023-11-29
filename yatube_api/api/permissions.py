from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешение, позволяющее изменять объект только владельцу."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
