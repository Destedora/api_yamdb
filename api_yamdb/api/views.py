from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .permissions import IsAdminIsModeratorIsAuthor
from .serializers import CommentSerializer
from reviews.models import Review


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для обработки запросов к комментариям.

    Позволяет создавать, просматривать, обновлять и удалять комментарии.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAdminIsModeratorIsAuthor]

    def get_review(self):
        """Возвращает объект отзыва через 'review_id' в URL."""
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Возвращает queryset комментариев для конкретного отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает новый комментарий к отзыву.

        Автор комментария автоматически устанавливается
        как текущий пользователь.
        """
        serializer.save(author=self.request.user, review=self.get_review())
