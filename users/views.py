from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import UserRegisterSerializer, UserLoginSerializer

# Template views: To be implemented
# def register_view(request):
#     return render(request, 'users/register.html')

# def login_view(request):
#     return render(request, 'users/login.html')

# def logout_view(request):
#     return render(request, 'users/logout.html')

class UserRegisterAPIView(generics.GenericAPIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            "user": user.username,
            "email": user.email,
            "message": "Account created"
        # "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_201_CREATED)


class UserLoginAPIView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)

        return super(UserLoginAPIView, self).post(request, format=None)


class UserLogoutAPIView(KnoxLogoutView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = self.request.user

        AuthToken.objects.filter(user=user).delete()
        logout(request)

        data = {'message': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

