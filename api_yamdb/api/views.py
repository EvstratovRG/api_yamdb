from rest_framework import viewsets, mixins

from reviews.models import Category, Genre, Title, Review, Comment, User
from . import serializers


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin):
    """Представление категорий."""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.CreateModelMixin):
    """Представление категорий."""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Представление произведений."""
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление произведений."""
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Представление произведений."""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Представление произведений."""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
