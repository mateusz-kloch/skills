from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from common.selectors import CustomArticleManager


class Article(models.Model):

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'articles'

    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    objects = models.Manager()
    verified_objects = CustomArticleManager()

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
        return ', '.join(
            tag.name for tag in self.tags.all()
        )


class Tag(models.Model):

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
