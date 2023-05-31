from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('pk', 'name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('pk', 'name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'rating',
                    'description', 'genre')
    search_fields = ('name', 'year', 'rating', 'genre', 'category')
    list_filter = ('pk', 'username', 'year', 'rating')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'score',
                    'pub_date')
    search_fields = ('pk', 'author', 'pub_date')
    list_filter = ('pk', 'author', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author',
                    'review', 'pub_date')
    search_fields = ('username',)
    list_filter = ('pk', 'author', 'pub_date')
    empty_value_display = '-пусто-'
