from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)
from reviews.validators import validate_year
from reviews.constants import MESSAGE_DUPLICATE_REVIEW


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категорий"""

    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Жанров"""

    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = ('name', 'slug')


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор Произведений для чтения"""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(required=False, default=None)

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
    """Сериализатор Произведений"""

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
        """Передаёт данные в сериализатор для чтения"""
        return GetTitleSerializer(instance).data

    @staticmethod
    def validate_year(value):
        """Проверяет, что заданный год не больше текущего"""
        return validate_year(value)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Отзывов"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """
        Проверяет, что пользователь не пытается
        добавить повторный отзыв
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
    """Сериализатор Комментариев"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
