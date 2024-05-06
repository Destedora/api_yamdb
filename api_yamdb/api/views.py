from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS
)
from rest_framework.pagination import LimitOffsetPagination

from api.filters import TitleFilter
from api.permissions import (
    IsAdminModeratorAuthor,
    IsAdminOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTitleSerializer,
    TitleSerializer,
    ReviewSerializer
)
from reviews.models import Category, Genre, Review, Title
from reviews.constants import ALLOW_METHODS


class BaseViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet
):
    """
    Базовый вьюсет для CategoryViewSet и GenreViewSet.
    """

    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)


class CategoryViewSet(BaseViewSet):
    """
    Вьюсет для модели категорий.
    """

    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class GenreViewSet(BaseViewSet):
    """
    Вьюсет для модели жанров.
    """

    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """
    Вьюсет для модели произведений.
    """

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('-year')
    http_method_names = ALLOW_METHODS
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """
        Определяет класс сериализатора для текущего запроса.
        """
        if self.request.method in SAFE_METHODS:
            return GetTitleSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """
    Вьюсет для модели отзывов.
    """

    serializer_class = ReviewSerializer
    http_method_names = ALLOW_METHODS
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthor
    ]

    def get_title(self):
        """
        Возвращает объект произведения через 'title_id' в URL.
        """
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """
        Получает набор отзывов для конкретного произведения.
        """
        return self.get_title().reviews.select_related('author')

    def perform_create(self, serializer):
        """
        Создает новый отзыв для указанного произведения.
        """
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(ModelViewSet):
    """
    Вьюсет для модели Комментариев.
    """

    serializer_class = CommentSerializer
    http_method_names = ALLOW_METHODS
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorAuthor
    ]

    def get_review(self):
        """
        Возвращает объект отзыва через 'review_id' в URL.
        """
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        """
        Получает набор комментариев для конкретного отзыва.
        """
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        """
        Создает новый комментарий для указанного отзыва.
        """
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
