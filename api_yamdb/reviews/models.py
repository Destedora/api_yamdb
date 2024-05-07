from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)
from django.db import models

from reviews.constants import (
    MESSAGE_MIN_VALUE,
    MESSAGE_MAX_VALUE,
    USERNAME_LENGTH,
    ROLE_MODERATOR,
    SYMBOLS_LENGTH,
    EMAIL_LENGTH,
    GENRE_LENGTH,
    TITLE_LENGTH,
    CODE_LENGTH,
    SLUG_LENGTH,
    ROLE_ADMIN,
    ROLE_USER,
    MIN_VALUE,
    MAX_VALUE
)
from reviews.validators import (
    validate_username,
    validate_year
)


class User(AbstractUser):
    """
    Кастомная модель пользователей.
    """
    class Role(models.TextChoices):
        """
        Перечисление ролей пользователя.
        """
        USER = ROLE_USER, 'User'
        ADMIN = ROLE_ADMIN, 'Admin'
        MODERATOR = ROLE_MODERATOR, 'Moderator'

    username = models.CharField(
        'Никнейм',
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=(validate_username,)
    )

    email = models.EmailField(
        'Электронная почта',
        help_text='Введите адрес электронной почты',
        max_length=EMAIL_LENGTH,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        help_text='Личная информация о пользователе',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(choice.value) for choice in Role),
        choices=Role.choices,
        default=Role.USER,
    )
    confirmation_code = models.CharField(
        max_length=CODE_LENGTH,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        """
        Проверяет, является ли пользователь обычным пользователем.
        """
        return self.role == self.Role.USER

    @property
    def is_moderator(self):
        """
        Проверяем является ли пользователь модератором.
        """
        return self.role == self.Role.MODERATOR

    @property
    def is_admin(self):
        """
        Проверяет, является ли пользователь администратором.
        """
        return (self.role == self.Role.ADMIN
                or self.is_superuser
                or self.is_staff)


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
                  'латиницы, цифры, дефис и подчёркивание.',
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:SYMBOLS_LENGTH]


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
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
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
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:SYMBOLS_LENGTH]


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
        ),
        db_index=True
    )

    class Meta(BaseReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_title_author_pair'
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
