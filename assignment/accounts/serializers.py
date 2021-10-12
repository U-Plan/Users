from .models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


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


class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        id = data.get("id")
        password = data.get("password")
        user = authenticate(username=id, password=password)

        if user and user.is_active:
            try:
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                update_last_login(None, user)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    'INVALID_ID_OR_PASSWORD'
                )
            return {
                'id': user.id,
                'token': jwt_token
            }
        raise serializers.ValidationError(
            'INVALID_ID_OR_PASSWORD')
