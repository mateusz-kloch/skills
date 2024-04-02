from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    pub_date = models.DateTimeField('date published')
    content = models.TextField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
    @admin.display(description='tags')
    def tags_as_str(self) -> str:
        """
        Returns names of all tags as a single string for an article.
        """
        return ', '.join(
            tag.name for tag in self.tags.all()
        )
    
    def get_related_tags(self) -> list['Tag']:
        return [tag for tag in self.tags.all()]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
