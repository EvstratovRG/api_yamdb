from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from . validators import validate_year, validate_me


CHOICES = [(i, i) for i in range(1, 11)]


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    user_role = ((USER, 'Аутентифицированный пользователь'),
                 (MODERATOR, 'Модератор'),
                 (ADMIN, 'Администратор'))

    username = models.CharField(
        verbose_name='Имя пользователя',
        blank=False,
        unique=True,
        validators=(validate_me, UnicodeUsernameValidator()),
        max_length=150,
        null=False
    )
    email = models.EmailField(
        verbose_name='email address',
        blank=False,
        unique=True,
        null=False
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.TextField(
        choices=user_role,
        default=USER,
        verbose_name='Права доступа',
    )
    confirmation_code = models.IntegerField(
        verbose_name='Подтверждающий код',
        default=11111
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER

    def __str__(self):
        return f'{self.username}'


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'


class Title(models.Model):
    """Наименование и атрибуты произведений."""
    name = models.CharField(max_length=256, blank=False)
    year = models.IntegerField(validators=[validate_year])
    rating = models.FloatField(null=True)
    description = models.TextField(max_length=300, blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    def __str__(self) -> str:
        return f'{self.name}'


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    """Отзывы пользователей на Title."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(choices=CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    # count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_review"
            )
        ]


class Comment(models.Model):
    """Комментарии пользователей к отзывам."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self) -> str:
        return self.text
