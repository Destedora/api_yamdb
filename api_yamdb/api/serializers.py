from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import serializers

from reviews.models import (
    User,
    Category,
    Genre,
    Title,
    Review,
    Comment,
)
from reviews.constants import (
    MESSAGE_DUPLICATE_USERNAME_EMAIL,
    MESSAGE_DUPLICATE_REVIEW,
    MESSAGE_BAD_CODE,
    USERNAME_LENGTH,
    EMAIL_LENGTH,
    CODE_LENGTH,
    MIN_VALUE,
    MAX_VALUE
)
from reviews.validators import (
    validate_year,
    validate_username
)

from api.utils import send_code


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для собственной модели пользователей.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователей.
    """

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
        model = User
        fields = ('email', 'username')

    def create(self, validated_data):
        """
        Создает пользователя или отправляет
        код подтверждения существующему.
        """
        user, _ = User.objects.get_or_create(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        send_code(user)
        return user

    def validate(self, data):
        """
        Проверяет данные перед созданием нового пользователя.
        """
        if User.objects.filter(**data):
            return data
        if User.objects.filter(
            username=data.get('username')
        ).exists() or User.objects.filter(
            email=data.get('email')
        ).exists():
            raise ValidationError(MESSAGE_DUPLICATE_USERNAME_EMAIL)
        return data


class GetTokenSerializer(serializers.Serializer):
    """
    Сериализатор для получения токена.
    """

    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=CODE_LENGTH,
        required=True
    )

    class Meta:
        fields = ('username', 'confirmation_code')

    def create(self, validated_data):
        """
        Создает токен доступа для пользователя.
        """
        return AccessToken.for_user(**validated_data)

    def validate(self, data):
        """
        Валидация данных при получении токена.
        """
        user = get_object_or_404(User, username=data.get('username'))
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError(MESSAGE_BAD_CODE)
        return {'user': user}


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий.
    """

    class Meta:
        model = Category
        lookup_field = 'slug'
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров.
    """

    class Meta:
        model = Genre
        lookup_field = 'slug'
        exclude = ('id',)


class GetTitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор произведений для чтения.
    """

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    rating = serializers.IntegerField(
        required=False,
        default=None
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор произведений.
    """

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False,
        allow_null=False
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def to_representation(self, instance):
        """
        Передаёт данные в сериализатор для чтения.
        """
        return GetTitleSerializer(instance).data

    @staticmethod
    def validate_year(value):
        """
        Проверяет, что заданный год не больше текущего.
        """
        return validate_year(value)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        min_value=MIN_VALUE,
        max_value=MAX_VALUE
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """
        Проверяет, что пользователь не пытается
        добавить повторный отзыв.
        """
        request = self.context.get('request')
        if request.method == 'POST':
            author = request.user
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(
                    title_id=title_id,
                    author=author
            ).exists():
                raise ValidationError(MESSAGE_DUPLICATE_REVIEW)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор комментариев.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
