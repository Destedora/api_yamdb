from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Настройка раздела пользователей.
    """

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'get_review_count',
        'get_comment_count',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name',
                     'role', 'bio',)
    list_filter = ('role',)

    @admin.display(description='Количество комментариев')
    def get_comment_count(self, obj):
        """
        Возвращает количество комментариев к объекту.
        """
        return obj.comments.count()

    @admin.display(description='Количество отзывов')
    def get_review_count(self, obj):
        """
        Возвращает количество отзывов к объекту.
        """
        return obj.reviews.count()
