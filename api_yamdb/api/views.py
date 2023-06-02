from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, mixins, filters
from reviews.models import Category, Genre, Title, Review, Comment
from . permissions import AdminOrReadOnly
from . import serializers


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin):
    """Представление категорий."""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.CreateModelMixin):
    """Представление категорий."""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)


class TitleViewSet(viewsets.ModelViewSet):
    """Представление произведений."""
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    serializer_class = serializers.TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление произведений."""
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    pagination_class = LimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    """Представление произведений."""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = LimitOffsetPagination


# class UserViewSet(viewsets.ModelViewSet):
#     """Представление произведений."""
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#     pagination_class = LimitOffsetPagination
