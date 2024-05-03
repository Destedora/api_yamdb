from django.contrib.auth import get_user_model
from django.db import models
from reviews.constants import (
    GENRE_LENGTH,
    SLUG_LENGTH,
    SYMBOLS_LENGTH,
    TITLE_LENGTH,
    MIN_VALUE,
    MAX_VALUE,
    MESSAGE_MIN_VALUE,
    MESSAGE_MAX_VALUE
)

User = get_user_model()


class BaseCategoryGenre(models.Model):
    """Базовая модель для Категорий и Жанров"""

    name = models.CharField(
        'Название',
        max_length=GENRE_LENGTH
    )
    slug = models.SlugField(
        'Слаг',
        max_length=SLUG_LENGTH,
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:SYMBOLS_LENGTH]


class BaseReviewComment(models.Model):
    """Базовая модель для Отзывов и Комментариев"""

    text = models.TextField(
        'Текст',
        help_text='Текст отзыва/комментария'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        help_text='Дата публикации отзыва/комментария',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:SYMBOLS_LENGTH]
