from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    BasePermission,
    SAFE_METHODS,
)


class IsAdmin(BasePermission):
    """
    Проверяет, является ли пользователь
    администратором или суперпользователем.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь право
        на выполнение действия.
        """
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_staff))


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
