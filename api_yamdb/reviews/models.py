from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import Truncator

from reviews.constants import (
    CHARFIELD_NAME_MAX_LENGTH,
    CHARFIELD_SLUG_MAX_LENGTH,
    SCORE_MIN_VALUE,
    SCORE_MAX_VALUE,
    STR_TEXT_TRUNCATE_CHARS
)
from reviews.validators import validate_film_year, validate_score


User = get_user_model()


User = get_user_model()


class NameSlugBaseModel(models.Model):
    name = models.CharField(
        max_length=CHARFIELD_NAME_MAX_LENGTH,
        verbose_name='Название',
        help_text='Введите название'
    )
    slug = models.SlugField(
        max_length=CHARFIELD_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Slug',
        help_text='Короткий идентификатор для URL'
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class TextAuthorPubDateModel(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ['pub_date']

    def __str__(self):
        return Truncator(self.text).chars(STR_TEXT_TRUNCATE_CHARS)


class Category(NameSlugBaseModel):

    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugBaseModel):

    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=CHARFIELD_NAME_MAX_LENGTH,
        verbose_name='Название произведения',
        help_text='Полное название фильма, сериала или книги'
    )
    year = models.PositiveSmallIntegerField(
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


class Review(TextAuthorPubDateModel):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
        help_text='Произведение, к которому относится отзыв'
    )
    score = models.PositiveSmallIntegerField(
        validators=[validate_score],
        verbose_name='Оценка',
        help_text=f'Оценка от {SCORE_MIN_VALUE} до {SCORE_MAX_VALUE}'
    )

    class Meta(TextAuthorPubDateModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(TextAuthorPubDateModel):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которому относится комментарий'
    )

    class Meta(TextAuthorPubDateModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
