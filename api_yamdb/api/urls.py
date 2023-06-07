from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    views.CommentViewSet,
    basename='comments')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/'
    r'(?P<review_id>\d+)/comments/(?P<comment_id>\d+)/comment',
    views.CommentViewSet,
    basename='comment')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments')
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', views.user_signup),
    path('v1/auth/token/', views.get_token),
    path('v1/', include(router.urls)),
]
