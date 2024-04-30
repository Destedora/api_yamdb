from django.contrib import admin

from .models import Review


@admin.register(Review)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки админки для модели Review."""

    list_display = ('pk', 'author', 'title', 'score', 'text', 'pub_date')
    search_fields = ('title', 'author', 'text', 'score')
    list_filter = ('title', 'author', 'score', 'pub_date',)
    empty_value_display = '-пусто-'
