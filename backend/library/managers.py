from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone


class CustomArticleManager(models.Manager):
    """
    A custom `Article` model manager.
    """
    def get_queryset(self) -> models.QuerySet:
        """
        Filters out defective articles.
        """
        return super().get_queryset().filter(
        pub_date__lte=timezone.now()
        ).exclude(
            title=''
        ).exclude(
            author__isnull=True
        ).exclude(
            tags__isnull=True
        ).exclude(
            content=''
        )
    

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
