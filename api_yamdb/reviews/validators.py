from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from reviews.constants import (
    MIN_SCORE,
    MAX_SCORE,
    FIRST_FILM,
    MIN_VALUE,
    MAX_VALUE
)


def characters_validator():
    return RegexValidator(
        r'^[-a-zA-Z0-9_]+$',
        _('Символы латинского алфавита, цифры и знак подчёркивания')
    )


def validate_film_year(value):
    current_year = timezone.now().year

    if not (MIN_VALUE <= value <= MAX_VALUE):
        raise ValidationError(_('Год должен быть четырехзначным числом'))

    if value < FIRST_FILM:
        raise ValidationError(_(
            f'Первый фильм был снят в {FIRST_FILM} году. '
            f'Вы указали: {value}'
        ))

    if value > current_year:
        raise ValidationError(_(
            f'Год не может быть больше {current_year}. '
            f'Вы указали: {value}'
        ))


def validate_score(value):
    if not MIN_SCORE <= value <= MAX_SCORE:
        raise ValidationError(
            _('Оценка должна быть от %(min)s до %(max)s.'),
            params={
                'min': MIN_SCORE,
                'max': MAX_SCORE,
                'value': value
            },
            code='invalid_score'
        )
