from .serializers import UserCreateSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response


class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'id': user.id}, status=status.HTTP_201_CREATED)
