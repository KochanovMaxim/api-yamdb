from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя для YaMDb."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )

    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email address'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='роль'
    )

    bio = models.TextField(
        blank=True,
        verbose_name='био'
    )

    confirmation_code = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='код подтверждения'
    )

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
