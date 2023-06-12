from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Доступ только администратор."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_superuser


class Moderator(permissions.BasePermission):
    """Доступ только администратор."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class Author(permissions.BasePermission):
    """Доступ только администратор."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class OnlyRead(permissions.BasePermission):
    """Доступ только для безопасных методов"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
