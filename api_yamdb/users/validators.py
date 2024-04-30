import re

from django.core.exceptions import ValidationError

from users.constants import (
    FORBIDDEN_USERNAME,
    MESSAGE_USERNAME,
    MESSAGE_SYMBOLS
)


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
