from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from .managers import CustomAccountManager


class Author(AbstractBaseUser, PermissionsMixin):
    
    class Meta:
        ordering = ['user_name']

    user_name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.user_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user_name)
        super().save(*args, **kwargs)
