from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)
from reviews.constants import (
    SYMBOLS_LENGTH,
    TITLE_LENGTH,
    MIN_VALUE,
    MAX_VALUE,
    MESSAGE_MIN_VALUE,
    MESSAGE_MAX_VALUE,
    GENRE_LENGTH,
    SLUG_LENGTH
)

from reviews.validators import validate_year


User = get_user_model()


class BaseCategoryGenre(models.Model):
    """
    Базовая модель для категорий и жанров.
    """

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
    """
    Базовая модель для отзывов и комментариев.
    """

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


class Category(BaseCategoryGenre):
    """
    Модель категорий.
    """

    class Meta(BaseCategoryGenre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseCategoryGenre):
    """
    Модель жанров.
    """

    class Meta(BaseCategoryGenre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Модель произведений.
    """

    name = models.CharField(
        'Название',
        max_length=TITLE_LENGTH
    )
    year = models.SmallIntegerField(
        'Год выпуска',
        help_text='Введите год, который не превышает текущий.',
        validators=(validate_year,),
        db_index=True
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('name',)

    def __str__(self):
        return self.name[:SYMBOLS_LENGTH]


class GenreTitle(models.Model):
    """
    Модель для связи id произведений и жанров.
    """

    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Связанный жанр/произведение'
        verbose_name_plural = 'Связанные жанры/произведения'
        ordering = ('title',)

    def __str__(self):
        return f'{self.genre} - {self.title}'


class Review(BaseReviewComment):
    """
    Модель отзывов.
    """

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        help_text=f'Укажите рейтинг произведения '
                  f'от {MIN_VALUE} до {MAX_VALUE}',
        validators=(
            MinValueValidator(MIN_VALUE, message=MESSAGE_MIN_VALUE),
            MaxValueValidator(MAX_VALUE, message=MESSAGE_MAX_VALUE)
        )
    )

    class Meta(BaseReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name="unique_title_author_pair"
            )
        ]

    def __str__(self):
        return (f'Рейтинг: {self.score} на {self.title} '
                f'от {self.author}')


class Comment(BaseReviewComment):
    """
    Модель комментариев.
    """

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE
    )

    class Meta(BaseReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return f'Комментарий на {self.review} от {self.author}'
