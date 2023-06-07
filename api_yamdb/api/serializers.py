import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


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
    """Сериализатор Пользователей"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        lookup_field = 'username'
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class UserSingUpSerializer(serializers.Serializer):
    """Сериализатор новых пользователей."""

    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=50, required=True)
    print('---13---')

    def validate(self, data):
        username = self.data['username']
        email = self.data['email']

    def vаlidate_username(self, data: object):
        username = data
        print('----1----')
        email = self.initial_data.get('email')
        print('----2----')
        if username == 'me':
            print('----3----')
            raise ValidationError(f'Логин {username} недоступен')
        if not re.match(r'^[\w.@+-]+\Z', username):
            print('----4----')
            raise serializers.ValidationError('Недопустимые символы')
        if User.objects.filter(
                username=username) and not User.objects.filter(
                email=email
        ):
            print('----5----')
            raise serializers.ValidationError(
                'Пользователь зарегистрирован с другой почтой'
            )
        if User.objects.filter(email=email) and not User.objects.filter(
                username=username
        ):
            print('----6----')
            raise serializers.ValidationError(
                'Пользователь зарегистрирован с другой почтой'
            )
        return data


class UserGetTokenSerializer(serializers.ModelSerializer):
    """Плучение Токена."""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
