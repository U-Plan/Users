from .serializers import UserCreateSerializer, UserSerializer
from .models import SmsAuthentication
from rest_framework import generics, status
from rest_framework.response import Response


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


class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'id': user.id}, status=status.HTTP_201_CREATED)
