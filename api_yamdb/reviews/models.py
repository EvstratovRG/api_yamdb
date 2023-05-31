from django.db import models

from users.models import User
from . validators import validate_year


CHOICES = [(i, i) for i in range(1, 11)]


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Наименование и атрибуты произведений."""
    name = models.CharField(max_length=256, blank=False)
    year = models.IntegerField(validators=[validate_year])
    raiting = models.FloatField()
    description = models.TextField(max_length=300, blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='ganres',
    )
    category = models.ManyToManyField(
        Category,
        related_name='categories',
    )

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """Отзывы пользователей на Title."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(choices=CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """Комментарии пользователей к отзывам."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text
