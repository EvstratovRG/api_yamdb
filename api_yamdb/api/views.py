from random import randint

from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status, filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Title, Review, Comment, User
from . import serializers, permissions
from .serializers import UserSingUpSerializer


class ListDestroyCreateWithFilters(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin
):
    """Класс представлений ListDestroyCreate с применением фильтрации."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (permissions.AdminOrReadOnly,)


class CategoryViewSet(ListDestroyCreateWithFilters):
    """Представление категорий."""

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(ListDestroyCreateWithFilters):
    """Представление категорий."""

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Представление произведений."""

    queryset = Title.objects.all().annotate(Avg('reviews__score')).\
        select_related('category').prefetch_related('genre')
    serializer_class = serializers.TitleSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug',)
    ordering_fields = ['name', 'year']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return serializers.TitleCreateAndUpdateSerializer
        return serializers.TitleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_slug = self.request.query_params.get('genre')
        category_slug = self.request.query_params.get('category')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление отзывов."""

    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthorOrAdminOrModerator,
                          IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        user = request.user

        if Review.objects.filter(author=user, title=title).exists():
            return Response(
                {'detail': 'Отзыв уже оставлен!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user, title=title)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление комментов к отзыву."""

    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthorOrAdminOrModerator,
                          IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)

    def create(self, request, *args, **kwargs):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, review=review)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UserViewSet(viewsets.ModelViewSet):
    """Представление пользователей."""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'delete', 'patch')

    @action(methods=['GET', 'PATCH'], detail=False,
            url_path='me', permission_classes=(IsAuthenticated,))
    def chang_user_fields(self, request):
        serializer = serializers.UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = serializers.UserSerializer(
                request.user,
                data=request.data,
                partial=True)
            if serializer.is_valid(raise_exception=True):
                if request.user.is_user or request.user.is_moderator:
                    serializer.save(role=request.user.role, partial=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup(request):
    """Представление регистрации пользователя."""

    serializer = UserSingUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    email = serializer.data['email']
    confirmation_code = randint(10000, 99999)
    try:
        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
    except IntegrityError:
        return Response('Указанные данные не корректны',
                        status=status.HTTP_400_BAD_REQUEST)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(subject='confirmation_code',
              message=f'Код: {confirmation_code}',
              from_email='yambd@gmail.com',
              recipient_list=[email])

    return Response(serializer.data,
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Представление получения токена."""

    serializer = serializers.UserGetTokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(User, username=serializer.data['username'])
    if serializer.data['confirmation_code'] == user.confirmation_code:
        token = RefreshToken.for_user(user).access_token
        return Response(f'Token: {token}',
                        status=status.HTTP_201_CREATED)
    else:
        return Response({'confirmation_code': 'Неверный код подтверждения!'},
                        status=status.HTTP_400_BAD_REQUEST)
