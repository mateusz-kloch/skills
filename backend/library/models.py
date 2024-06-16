from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from .managers import CustomArticleManager, CustomAccountManager


class Article(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    objects = models.Manager()
    verified_objects = CustomArticleManager()

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'articles'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @admin.display(description='tags')
    def tags_as_str(self) -> str:
        """
        Returns names of all tags related with an article as a single string.
        """
        return ', '.join(tag.name for tag in self.tags.all())
    

class Author(AbstractBaseUser, PermissionsMixin):
    DEFAULT_AVATAR = 'static/library/author/default/default_avatar.png'

    def create_avatar_path(instance, filename):
        """
        Creates a path where Author avatar will be uploaded.
        """
        return f'static/library/author/{instance.user_name}/{filename}'

    user_name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    avatar = models.ImageField(default=DEFAULT_AVATAR, upload_to=create_avatar_path)
    joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['user_name']

    def __str__(self):
        return self.user_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user_name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
