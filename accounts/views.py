from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User
from config.exceptions import BadRequestException

from .serializers import LoginSerializer, RegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken




class RegistrationView(APIView):
    def post(self, request):  
        self.validate_fields(request.data)
        serializer = RegistrationSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def validate_fields(self, data):
        if(not data.get('email') or not data.get('full_name') or not data.get('username') or not data.get('password')):
            raise BadRequestException("All fields are required.")
        
        if User.objects.filter(email = data.get('email')).exists():
            raise BadRequestException("User with this email already exists.")
    
        if User.objects.filter(username = data.get('username')).exists():
            raise BadRequestException("User with this username already exists.")
        
        if len(data.get('password', '')) < 6:
            raise BadRequestException("Password must be at least 6 characters long.")
        
        if len(data.get('full_name', '')) < 3:
            raise BadRequestException("Full name must be at least 3 characters long.")

class LoginView(APIView):
    def post(self, request):
        self.validate_fields(request.data)
        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "isSuccess": True,
                "message": "Login successful.",
                "user": {
                    "id" : user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "username": user.username,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
            }}, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def validate_fields(self, data):
        if not data.get('email') or not data.get('password'):
            raise BadRequestException("Email and password are required.")
        
        if len(data.get('password', '')) < 6:
            raise BadRequestException("Password must be at least 6 characters long.")
        

# Create your views here.
