from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки админки для модели Comment."""

    list_display = ('pk', 'author', 'review', 'text', 'pub_date')
    search_fields = ('review', 'author', 'text')
    list_filter = ('review', 'author', 'pub_date',)
    empty_value_display = '-пусто-'
