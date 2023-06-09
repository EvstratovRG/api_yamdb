import re

from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = timezone.now().year
    if value < 1900 or value > current_year:
        raise ValidationError(
            'Неверно указан год, не может быть меньше 1900 и больше текущего.'
        )


def validate_me(username):
    if username == 'me':
        raise ValidationError('Недопустимое имя пользователя!')

    if re.search(r'^[\w.@+-]+\Z', username) is None:
        raise ValidationError(
            f'Не допустимые символы <{username}> в нике.'
        )
