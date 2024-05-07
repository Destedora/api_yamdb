import re
from django.utils import timezone

from django.core.exceptions import ValidationError

from .constants import (
    FORBIDDEN_USERNAME,
    MESSAGE_USERNAME,
    MESSAGE_SYMBOLS
)


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


def validate_username(username):

    if username == FORBIDDEN_USERNAME:
        raise ValidationError(
            {'username': MESSAGE_USERNAME},
        )
    forbidden_symbols = re.sub(r'^[\w.@+-]+\Z', '', username)
    if forbidden_symbols:
        raise ValidationError(
            {'username': MESSAGE_SYMBOLS.format(
                username=username,
                symbols=''.join(set(forbidden_symbols))
            )},
        )
    return username
