from rest_framework import serializers

from config.exceptions import BadRequestException
from .models import User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'username', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email= validated_data['email'],
            full_name = validated_data['full_name'],
            username = validated_data['username'],
            password = validated_data['password']
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only= True)

    def validate(self, data):
        user = authenticate(email = data['email'], password = data['password'])

        if not user:
            raise BadRequestException("Invalid email or password.")
        
        return user