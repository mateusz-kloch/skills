from django.contrib import admin

from .models import Article, Tag


class ArticleAdminConfig(admin.ModelAdmin):
    """
    A custom view of articles for an admin.
    """
    search_fields = ('title', 'author')
    fieldset = [('Article informations', {'fields': [
        'title', 'slug', 'author', 'tags', 'pub_date', 'content'
    ]})]
    filter_horizontal = ['tags']
    list_display = [
        'title', 'author', 'pub_date', 'tags_as_str'
    ]
    list_filter = ['author', 'pub_date', 'tags']


admin.site.register(Article, ArticleAdminConfig)
admin.site.register(Tag)
