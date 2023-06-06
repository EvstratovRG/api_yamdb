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


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор Пользователей"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        lookup_field = 'username'
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class UserSingUpSerializer(serializers.ModelSerializer):
    """Сериализатор новых пользователей."""

    class Meta:
        model = User
        fields = ('email', 'username')


    # username = serializers.CharField(max_length=150, required=True)
    # email = serializers.EmailField(max_length=150, required=True)
    #
    # def vаlidate_username(self, value):
    #     if User.objects.filter(username__iexact=value).exists():
    #         raise serializers.ValidationError('Пользователь с именем: '
    #                                           f'{username}, уже существует')
    #     if username == 'me':
    #         raise serializers.ValidationError('Такое имя не доступно')
    #     return username
    #
    # def validate_email(self, value):
    #     if User.objects.filter(email__iexact=value).exists():
    #         raise serializers.ValidationError('Адрес: '
    #                                           f'{email} уже используетс')
    #     return email


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