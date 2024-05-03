from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from users.models import CustomUser
from users.constants import (
    CODE_LENGTH,
    USERNAME_LENGTH,
    EMAIL_LENGTH,
    MESSAGE_DUPLICATE_USERNAME,
    MESSAGE_DUPLICATE_EMAIL
)
from users.validators import validate_username
from users.utils import send_code


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для собственной модели Пользователей"""

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации Пользователей"""

    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True,
        validators=[
            validate_username,
            UnicodeUsernameValidator()
        ]
    )
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def create(self, validated_data):
        """
        При создании пользователя отправляет
        код на адрес электронной почты
        """
        user = CustomUser.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        send_code(user)
        return user

    def validate(self, data):
        """Проверяет данные перед созданием нового пользователя"""
        if CustomUser.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(MESSAGE_DUPLICATE_USERNAME)
        elif CustomUser.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(MESSAGE_DUPLICATE_EMAIL)
        return data


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения Токена"""

    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=CODE_LENGTH,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
