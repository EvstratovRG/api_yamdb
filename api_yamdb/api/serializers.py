from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slag')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slag')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    class Meta:
        model = Title
        fields = ()


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов пользователей."""

    class Meta:
        model = Review
        fields = ()


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев к отзывам."""

    class Meta:
        model = Comment
        fields = ()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев к отзывам."""

    class Meta:
        model = User
        fields = ()


class UserSingUpSerializer(serializers.Serializer):
    """Сериализатор новых пользователей."""

    username = serializers.CharField(max_length=254, required=True)
    email = serializers.EmailField(max_length=150, required=True)

