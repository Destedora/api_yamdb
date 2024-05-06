from django.contrib import admin

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)

admin.site.empty_value_display = 'Не задано'


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
