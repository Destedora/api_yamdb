from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrReadOnly


class BaseViewSet(
    CreateModelMixin, DestroyModelMixin,
    ListModelMixin, GenericViewSet
):
    """Базовый вьюсет для CategoryViewSet и GenreViewSet"""

    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
