from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission
)


class IsAdminOrReadOnly(BasePermission):
    """
    Предоставляет полный доступ администратору,
    остальным пользователям - только чтение
    """

    def has_permission(self, request, view):
        """Проверяет разрешение для доступа к представлению"""
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated and
                request.user.is_admin
            )
        )


class IsAdminModeratorAuthor(BasePermission):
    """
    Предоставляет полуный доступ администратору, модератору
    или автору, остальным пользователям - только чтение
    """

    def has_object_permission(self, request, view, obj):
        """Проверяет разрешение для доступа к конкретному объекту"""
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
