from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    user_role = ((USER, 'Аутентифицированный пользователь'),
                 (MODERATOR, 'Модератор'),
                 (ADMIN, 'Администратор'))

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        null=False,
        unique=True
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

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_mderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
