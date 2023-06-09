# import re

# from django.core.exceptions import ValidationError
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
    """Сериализатор пользователей."""

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

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Аккаунт с таким email уже существует.'
            )
        return value

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        lookup_field = 'username'
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class UserSingUpSerializer(serializers.Serializer):
    """Сериализатор новых пользователей."""

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_me]
    )
    email = serializers.EmailField(max_length=50, required=True)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists()\
                and not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь зарегистрирован с другой почтой'
            )
        if User.objects.filter(email=email).exists()\
                and not User.objects.filter(username=username).exists():
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


class TitleCreateAndUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания или редактирования произведения."""

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

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def get_author(self, obj):
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
        fields = ('id', 'text', 'author', 'pub_date',)
