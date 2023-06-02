from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, mixins, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, Review, Comment, User
from . import serializers, permissions


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin):
    """Представление категорий."""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.CreateModelMixin):
    """Представление категорий."""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
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


class UserViewSet(viewsets.ModelViewSet):
    """Представление произведений."""
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = LimitOffsetPagination


@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup(request):
    serializer = serializers.UserSingUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data['username']
        email = serializer.data['email']
        confirmation_code = randint(100000, 999999)
        try:
            User.objects.get_or_create(username=username,
                                       email=email,
                                       confirmation_code=confirmation_code)
        except ValueError as error:
            return Response({f'Введены не корректные данные{error}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        send_mail(subject='confirmation_code',
                  message=f'Код: {confirmation_code}',
                  from_email='yambd@gmail.com',
                  recipient_list=[email])

    return Response({'Пользователь зарегистрирован.'
                     f' Код подтверждения отправлен {email}'},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = serializers.UserGetTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=serializer.data['username'])
    if serializer.data['confirmation_code'] == user.confirmation_code:
        token = RefreshToken.for_user(user).access_token
        return Response(f'Token: {token}',
                        status=status.HTTP_201_CREATED)
    else:
        Response({'confirmation_code': 'Неверный код подтверждения!'},
                 status=status.HTTP_400_BAD_REQUEST)

