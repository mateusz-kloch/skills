from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='articles')
    pub_date = models.DateTimeField('date published', default=timezone.now)
    content = models.TextField()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
    
    @admin.display(description='tags')
    def tags_as_str(self) -> str:
        """
        Returns names of all tags related with an article as a single string.
        """
        return ', '.join(
            tag.name for tag in self.tags.all()
        )


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
