from .models import User
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],
            nickname=validated_data['nickname'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ['nickname', 'email', 'name', 'phone', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'email', 'name', 'phone']
