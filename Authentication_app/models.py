from django.db import models
from django.utils import timezone
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    
    def create_user(self, Email, password=None, **extra_fields):
        if not Email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(Email)
        user = self.model(Email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(Email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    Name = models.CharField(max_length=150,blank=False)
    Email = models.EmailField(unique=True, blank=False)
    Username = models.CharField(unique=True, max_length=150, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    Phone = models.CharField(max_length=10, blank=False, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.Email