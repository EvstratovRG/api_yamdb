from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Доступ администратор или только безопасные HTTP методы."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class AdminOnly(permissions.BasePermission):
    """Доступ только администратор."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_superuser


class ModeratorOrReadOnly(permissions.BasePermission):
    """Доступ только администратор."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class AuthorOrReadOnly(permissions.BasePermission):
    """Доступ только администратор."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)
