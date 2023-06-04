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
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        lookup_field = 'username'
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class UserSingUpSerializer(serializers.Serializer):
    """Сериализатор новых пользователей."""

    username = serializers.CharField(max_length=254, required=True)
    email = serializers.EmailField(max_length=150, required=True)


class UserGetTokenSerializer(serializers.Serializer):
    """Плучение Токена."""

    username = serializers.CharField(max_length=254, required=True)
    confirmation_code = serializers.IntegerField(max_value=999999,
                                                 min_value=100000,
                                                 required=True)
