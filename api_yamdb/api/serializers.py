from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment, User


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
        fiedls = ()


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
