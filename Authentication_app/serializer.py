from rest_framework import serializers
from .models import *
import re
from django.core.exceptions import ValidationError


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
        print(validated_data,'validate data')
        user = CustomUser.objects.create_user(
            Name=validated_data['Name'],
            Username=validated_data['Username'],
            Email=validated_data['Email'],
            Phone=validated_data['Phone'],
            password=validated_data['password'],
        )
        user.save()
        return user
