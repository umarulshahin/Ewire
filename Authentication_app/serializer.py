from rest_framework import serializers
from .models import *
import re
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = CustomUser
        fields = ['Name','Email', 'Username' , 'Phone', 'password','id']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def validate(self, attrs):
        
            password = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

            if not re.match(password,attrs['password']):
                raise ValidationError("Password must be at least 8 characters long, contain at least one letter, one number, and one special character.")
        
            if CustomUser.objects.filter(Username=attrs['Username']).exists():
                raise ValidationError({"email": "Username already exists."})
            
            if CustomUser.objects.filter(Email=attrs['Email']).exists():
                raise ValidationError({"email": "Email already exists."})
            
            if CustomUser.objects.filter(Phone=attrs['Phone']).exists():
                raise ValidationError({"phone": "Phone number already exists."})
            return attrs
           
    def create(self, validated_data):
        
        user = CustomUser.objects.create_user(
            Name=validated_data['Name'],
            Username=validated_data['Username'],
            Email=validated_data['Email'],
            Phone=validated_data['Phone'],
            password=validated_data['password'],
        )
        user.save()
        return user

class CustomTokenSerializer(serializers.Serializer):
    Username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('Username')
        password = data.get('password')
  
        user = authenticate(Username=username,password=password)
        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid username or password, or user not active.")
            
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.Username

        return {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.Username,
            }
        