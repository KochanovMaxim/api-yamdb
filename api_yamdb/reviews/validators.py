from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from reviews.constants import (
    SCORE_MIN_VALUE,
    SCORE_MAX_VALUE,
)


def validate_film_year(value):
    current_year = timezone.now().year

    if value > current_year:
        raise ValidationError(_(
            f'Год не может быть больше {current_year}. '
            f'Вы указали: {value}'
        ))


def validate_score(value):
    if not SCORE_MIN_VALUE <= value <= SCORE_MAX_VALUE:
        raise ValidationError(
            _('Оценка должна быть от %(min)s до %(max)s.'),
            params={
                'min': SCORE_MIN_VALUE,
                'max': SCORE_MAX_VALUE,
                'value': value
            },
            code='invalid_score'
        )
