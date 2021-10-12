from .serializers import UserCreateSerializer, UserSerializer, UserLoginSerializer
from .models import SmsAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.validators import RegexValidator, ValidationError


@permission_classes([AllowAny])
class SmsAuth(generics.GenericAPIView):
    def post(self, request):
        try:
            phone = request.data['phone']
        except KeyError:
            return Response({'message': 'INVALID_VALUE'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            SmsAuthentication.objects.update_or_create(phone=phone)
        return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            check_phone = request.query_params['phone']
            check_number = request.query_params['auth']
        except KeyError:
            return Response({'message': 'INVALID_VALUE'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            auth_key = SmsAuthentication.check_sms_auth(
                check_phone, check_number)
            return Response({'auth_key': auth_key}, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        password_validator = RegexValidator(
            regex="^[A-Za-z0-9!@#$%^&+=]{8,100}$")
        try:
            password_validator(request.data['password'])
            auth_key = request.data['auth']
            check_phone = request.data['phone']
        except ValidationError:
            return Response({'message': 'INVALID_PASSWORD'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except KeyError:
            return Response({'message': 'INVALID_VALUE'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        result = SmsAuthentication.check_auth_key(check_phone, auth_key)

        if not result:
            return Response({'message': 'INVALID_AUTH'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'id': user.id}, status=status.HTTP_201_CREATED)


@permission_classes([AllowAny])
class UserLogin(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if not user:
            return Response({'message': 'INVALID_VALUE'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'token': user['token']}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class UserInfo(generics.GenericAPIView):
    serial = UserSerializer

    def get(self, request):
        return Response({'info': UserSerializer(request.user, context=self.get_serializer_context()).data}, status=status.HTTP_200_OK)

    def patch(self, request):
        password_validator = RegexValidator(
            regex="^[A-Za-z0-9!@#$%^&+=]{8,100}$")
        try:
            password_validator(request.data['password'])
            auth_key = request.data['auth']
            check_phone = request.data['phone']
        except ValidationError:
            return Response({'message': 'INVALID_PASSWORD'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except KeyError:
            return Response({'message': 'INVALID_VALUE'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        result = SmsAuthentication.check_auth_key(check_phone, auth_key)

        if not result:
            return Response({'message': 'INVALID_AUTH'}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        user.set_password(request.data['password'])
        user.save()
        return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)
