from django.contrib.auth.models import(
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db import models
from django.utils import timezone


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, user_name, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to `is_superuser=True`.')
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to `is_staff=True`.')
        
        return self.create_user(user_name, email, password, **other_fields)
    
    def create_user(self, user_name, email, password, **other_fields):
        email = self.normalize_email(email)

        user = self.model(user_name=user_name, email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user
    

class Author(AbstractBaseUser, PermissionsMixin):
    
    class Meta:
        ordering = ['user_name']

    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.user_name
