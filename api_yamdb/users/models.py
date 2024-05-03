from django.contrib.auth.models import AbstractUser
from django.db import models


from users.constants import (
    USER,
    MODERATOR,
    ADMIN,
    ROLES,
    USERNAME_LENGTH,
    EMAIL_LENGTH,
    CODE_LENGTH
)
from users.validators import validate_username


class CustomUser(AbstractUser):
    """Кастомная модель Пользователей."""

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
        max_length=max(len(role[0]) for role in ROLES),
        choices=ROLES,
        default=USER,
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
        return self.role == USER

    @property
    def is_moderator(self):
        """Проверяем является ли пользователь модератором"""
        return self.role == MODERATOR

    @property
    def is_admin(self):
        """Проверяем является ли пользователь админом или суперюзером"""
        return self.role == ADMIN or self.is_superuser
