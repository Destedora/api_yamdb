from rest_framework.permissions import BasePermission


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
