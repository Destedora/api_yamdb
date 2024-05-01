from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.constants import MAX_NAME_LENGTH
from users.models import CustomUser
from .validators import validate_username


class TokenSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения токена."""

    class Meta:
        model = CustomUser
        fields = ('username',)


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено'
            )
        if CustomUser.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Такой пользователь с таким ником уже существует'
            )
        if CustomUser.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистриорван'
            )
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для собственной модели юзера."""

    username = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
        required=True,
        validators=[
            validate_username,
            UniqueValidator(queryset=CustomUser.objects.all()),
        ]
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
