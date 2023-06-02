from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'rating',
                    'description')
    search_fields = ('name', 'year', 'rating',)
    list_filter = ('year', 'rating',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'score',
                    'pub_date')
    search_fields = ('pk', 'author', 'pub_date',)
    list_filter = ('author', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author',
                    'review', 'pub_date')
    search_fields = ('username',)
    list_filter = ('author', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'confirmation_code',
                    'first_name', 'last_name', 'password')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
