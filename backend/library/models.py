from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils import timezone


class Article(models.Model):

    class VerifiedArticles(models.Manager):
        """
        Filters out defective articles.
        """
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(
            pub_date__lte=timezone.now()
        ).exclude(
            title=''
        ).exclude(
            tags__isnull=True
        ).exclude(
            content=''
        )

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'articles'

    title = models.CharField(max_length=150)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    objects = models.Manager()
    verified_objects = VerifiedArticles()        

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

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
