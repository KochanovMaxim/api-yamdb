from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from reviews.constants import FORBIDDEN_USERNAME


def validate_username_not_me(value):
    if value == FORBIDDEN_USERNAME:
        raise ValidationError(
            _('Имя пользователя "%(value)s" запрещено.'),
            params={'value': value},
        )
