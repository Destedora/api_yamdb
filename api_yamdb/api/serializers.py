from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов.

    Включает в себя имя автора отзыва и позволяет преобразовывать
    данные комментария в JSON и обратно. Автор и дата публикации
    являются только для чтения.
    """
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('pub_date',)
