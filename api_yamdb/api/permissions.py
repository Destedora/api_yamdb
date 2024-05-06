from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly
)
from users.permissions import IsAdmin


class IsAdminOrReadOnly(IsAdmin):
    """
    Предоставляет полный доступ администратору,
    остальным пользователям - только чтение.
    """

    def has_permission(self, request, view):
        """
        Проверяет, что пользователь является администратором,
        либо метод безопасен.
        """
        return (request.method in SAFE_METHODS
                or super().has_permission(request, view))


class IsAdminModeratorAuthor(IsAuthenticatedOrReadOnly):
    """
    Предоставляет полный доступ администратору, модератору,
    автору, остальным пользователям - только чтение.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, что пользователь является администратором,
        модератором, автором контента, либо метод безопасен.
        """
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)
