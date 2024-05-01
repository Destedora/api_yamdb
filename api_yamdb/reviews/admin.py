from django.contrib import admin

from reviews.models import (
    Category, Comment,
    Genre, GenreTitle,
    Review, Title
)

admin.site.empty_value_display = 'Не задано'


class GenreTitleInline(admin.StackedInline):
    """
    Отображение и редактирование связанных объектов
    GenreTitle в административном интерфейсе
    """

    model = GenreTitle
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка раздела Категорий"""

    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка раздела Жанров"""

    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')
    inlines = (GenreTitleInline,)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка раздела Произведений"""

    list_display = ('name', 'year', 'description', 'category',)
    search_fields = ('name',)
    list_filter = ('name', 'year', 'category',)
    list_editable = ('category',)
    inlines = (GenreTitleInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка раздела Отзывов"""

    list_display = ('title', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('title', 'author', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка раздела Комментариев"""

    list_display = ('review', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author', 'review', 'pub_date',)
