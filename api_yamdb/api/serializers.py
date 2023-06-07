import re

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title, Review, Comment, User
from reviews.validators import validate_me, validate_year


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
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор Пользователей"""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            validate_me,
            UniqueValidator(queryset=User.objects.all()),
        ]
    )
    email = serializers.CharField(
        max_length=254,
        required=True,
        validators=[UniqueValidator]
    )

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

    def validate_username(self, data):
        username = data
        email = self.initial_data.get('email')
        if username == 'me':
            raise ValidationError(f'Логин {username} недоступен')
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError('Недопустимые символы')
        if User.objects.filter(
                username=username) and not User.objects.filter(
                email=email
        ):
            raise serializers.ValidationError(
                'Пользователь зарегистрирован с другой почтой'
            )
        if User.objects.filter(email=email) and not User.objects.filter(
                username=username
        ):
            raise serializers.ValidationError(
                'Пользователь зарегистрирован с другой почтой'
            )
        return data



class UserGetTokenSerializer(serializers.ModelSerializer):
    """Плучение Токена."""

    username = serializers.CharField(max_length=254, required=True)
    confirmation_code = serializers.IntegerField(max_value=999999,
                                                 min_value=100000,
                                                 required=True)
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class TitleCreateAndUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SerializerMethodField()

    def get_author(self, obj):  # метод достает только username из словаря
        return obj.author.username

    class Meta:
        model = Review
        fields = ['id', 'title', 'author', 'text', 'score', 'pub_date']
        extra_kwargs = {
            'title': {'required': False},
            'count': {'required': False},
        }


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')