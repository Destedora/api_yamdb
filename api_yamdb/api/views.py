from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .permissions import IsAdminIsModeratorIsAuthor
from .serializers import ReviewSerializer
from .validators import validate_unique_review
from reviews.models import Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки запросов к отзывам.

    Позволяет создавать, просматривать, обновлять и удалять отзывы.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminIsModeratorIsAuthor]

    def get_title(self):
        """Возвращает объект произведения через 'title_id' в URL."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Возвращает queryset отзывов для конкретного произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Сохранение нового отзыва с автором и произведением.

        Валидация на уникальность отзыва.
        """
        title = self.get_title()
        user = self.request.user
        validate_unique_review(user, title.id)
        serializer.save(author=user, title=title)
