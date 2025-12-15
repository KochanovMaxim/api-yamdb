from django.contrib.auth.models import AbstractUser
from django.db import models
from reviews.constants import (
    USERNAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    ROLE_MAX_LENGTH,
    ROLE_CHOICES,
    USER,
    MODERATOR,
    ADMIN
)
from users.validators import validate_username_not_me


class User(AbstractUser):
    ROLE_CHOICES = ROLE_CHOICES

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text='Обязательное поле. 150 символов или меньше.',
        validators=[validate_username_not_me],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )

    email = models.EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        verbose_name='email address'
    )

    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='роль'
    )

    bio = models.TextField(
        blank=True,
        verbose_name='био'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.is_authenticated and
            (self.is_superuser or self.is_staff or self.role == ADMIN)
        )

    @property
    def is_moderator(self):
        return (
            self.is_authenticated and
            self.role == MODERATOR
        )
