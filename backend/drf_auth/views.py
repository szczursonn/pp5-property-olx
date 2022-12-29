from django.contrib.auth import login, logout
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer

class LoginView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(
            data=self.request.data,
            context={ 'request': self.request }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = RegisterSerializer(
            data=self.request.data,
            context={'request':self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_201_CREATED)
