from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns = [
    path('auth', views.SmsAuth.as_view()),
    path('auth/certificate', views.SmsCertificate.as_view()),
    path('signup', views.UserCreate.as_view()),
    path('login', views.UserLogin.as_view()),
    path('info', views.UserInfo.as_view()),
]
