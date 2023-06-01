from random import randint

from django.core.mail import send_mail
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User
from . import serializers, permissions


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


@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup(request):
    serializer = serializers.UserSingUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data['username']
        email = serializer.data['email']
        confirmation_code = randint(100000, 999999)
        User.objects.get_or_create(username=username, email=email)
        send_mail(subject='confirmation_code',
                  message=f'Код: {confirmation_code}',
                  from_email='yambd@gmail.com',
                  recipient_list=[email])

