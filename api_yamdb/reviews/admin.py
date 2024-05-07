from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import (
    User,
    Category,
    Genre,
    Title,
    Review,
    Comment
)

admin.site.empty_value_display = 'Не задано'


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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Настройка раздела категорий.
    """

    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name', 'slug',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Настройка раздела жанров.
    """

    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name', 'slug',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """
    Настройка раздела произведений.
    """

    list_display = ('name', 'year', 'description', 'category',)
    search_fields = ('name',)
    list_filter = ('name', 'year', 'category',)
    list_editable = ('category',)

    @admin.display(description='Жанр')
    def get_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Настройка раздела отзывов.
    """

    list_display = (
        'title',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('text',)
    list_filter = ('title', 'author', 'score', 'pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Настройка раздела комментариев.
    """

    list_display = (
        'review',
        'author',
        'pub_date',
    )
    search_fields = ('text',)
    list_filter = ('author', 'review', 'pub_date',)
