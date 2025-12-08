from django.db import models
from django.contrib.auth import get_user_model

from reviews.validators import (
    characters_validator,
    validate_film_year,
    validate_score
)
from reviews.constants import (
    CHARFIELD_NAME_MAX_LENGTH,
    CHARFIELD_SLUG_MAX_LENGTH,
)


User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=CHARFIELD_NAME_MAX_LENGTH,
        verbose_name='Название категории',
        help_text='Например: Фильмы, Сериалы, Книги'
    )
    slug = models.SlugField(
        max_length=CHARFIELD_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Slug категории',
        validators=[characters_validator],
        help_text='Короткий идентификатор для URL'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=CHARFIELD_NAME_MAX_LENGTH,
        verbose_name='Название жанра',
        help_text='Например: Комедия, Драма, Фантастика'
    )
    slug = models.SlugField(
        max_length=CHARFIELD_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Slug жанра',
        validators=[characters_validator],
        help_text='Короткий идентификатор для URL'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=CHARFIELD_NAME_MAX_LENGTH,
        verbose_name='Название произведения',
        help_text='Полное название фильма, сериала или книги'
    )
    year = models.IntegerField(
        validators=[validate_film_year],
        verbose_name='Год выпуска',
        help_text='Год первого выпуска произведения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Подробное описание сюжета, актёров, режиссёра'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='titles',
        help_text='Выберите один или несколько жанров'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='titles',
        help_text='Выберите категорию произведения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
        help_text='Произведение, к которому относится отзыв'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Подробный отзыв о произведении'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews',
        help_text='Автор отзыва'
    )
    score = models.IntegerField(
        validators=[validate_score],
        verbose_name='Оценка',
        help_text='Оценка от 1 до 10'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        help_text='Дата и время публикации отзыва'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которому относится комментарий'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст вашего комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
        help_text='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        help_text='Дата и время публикации комментария'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
