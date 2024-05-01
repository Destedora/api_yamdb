from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    """Проверяет, что год не больше текущего."""
    if value > timezone.now().year:
        raise ValidationError(
            f'Значение введенного года {value} '
            f'не может быть больше текущего',
            params={'value': value},
        )
    return value
