from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Проверяет, является пользователь
    администратором или суперпользователем
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь право
        на выполнение действия
        """
        return (
                request.user.is_authenticated and
                (request.user.is_superuser or request.user.is_admin)
        )
