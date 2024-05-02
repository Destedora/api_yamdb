from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментария.

    Включает в себя имя автора комментария и позволяет преобразовывать
    данные комментария в JSON и обратно. Автор, связанный отзыв
    и дата публикации являются только для чтения.
    """
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'pub_date',)
