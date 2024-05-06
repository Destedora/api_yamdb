from django.contrib.auth.models import AbstractUser
from django.db import models


from users.constants import (
    ROLE_USER,
    ROLE_MODERATOR,
    ROLE_ADMIN,
    USERNAME_LENGTH,
    EMAIL_LENGTH,
    CODE_LENGTH
)
from users.validators import validate_username


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
        'Код подтверждения',
        max_length=CODE_LENGTH,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

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
