from reviews.models import Review
from rest_framework.exceptions import ValidationError


def validate_unique_review(user, title_id):
    """ Проверка уникальности отзыва.

    Проверяет, оставил ли пользователь отзыв на произведение.
    Вызывает ValidationError, если отзыв уже существует.
    """
    if Review.objects.filter(title_id=title_id, author=user).exists():
        raise ValidationError('Вы уже оставляли отзыв на это произведение.')
