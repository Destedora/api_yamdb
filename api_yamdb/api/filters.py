from django_filters import (
    CharFilter,
    FilterSet,
    NumberFilter
)

from reviews.models import Title


class TitleFilter(FilterSet):
    """
    Фильтр для модели произведений.
    """

    category = CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='contains'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = NumberFilter(
        field_name='year',
        lookup_expr='exact')

    class Meta:
        model = Title
        exclude = '__all__'
