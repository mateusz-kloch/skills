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
