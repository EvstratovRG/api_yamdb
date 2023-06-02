from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('v1/auth/signup/', views.user_signup),
    path('v1/auth/token/', views.get_token),
]

