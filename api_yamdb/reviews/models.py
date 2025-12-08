from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        vebrose_name='Название',
        max_length=256,
        help_text='Выберите категорию'
    )
    slug = models.SlugField(
        vebrose_name='Слаг',
        max_length=56,
        unique=True,
        help_text='Символы латинского алфавита, цифры и знак подчёркивания'

    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    pass


class Titles(models.Model):
    pass


class Reviews(models.Model):
    pass


class Comments(models.Model):
    pass
