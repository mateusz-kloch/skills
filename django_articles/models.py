from django.contrib import admin
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=250)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField('date published')
    content = models.TextField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
    @admin.display(description='tags')
    def tags_as_str(self):
        return ', '.join(tag.name for tag in self.tags.all())
