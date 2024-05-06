from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Проверяет, что заданный год не больше текущего.
    """
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'Значение введенного года {value} '
            f'не может быть больше {current_year}',
            params={'value': value},
        )
    return value
