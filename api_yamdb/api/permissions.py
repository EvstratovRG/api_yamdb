from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Доступ администратор или только безопасные HTTP методы."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class AdminOnly(permissions.BasePermission):
    """Доступ только администратор."""

    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.is_admin)
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.user.is_authenticated and request.user.is_admin)
            or request.user.is_staff
        )


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """Доступ автору, модератору или администратору,
    либо только безопасные HTTP методы."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'POST' and request.user.is_authenticated
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
