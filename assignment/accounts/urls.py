from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns = [
    path('auth/', views.SmsAuth.as_view()),
    path('signup/', views.UserCreate.as_view()),
]
