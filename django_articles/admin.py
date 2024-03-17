from django.contrib import admin

from .models import Article, Tag


class ArticleAdmin(admin.ModelAdmin):
    fieldset = [
        (
            'Article informations', {
                'fields': [
                    'title',
                    'tags',
                    'date_published',
                    'content'
                ]
            }
        )
    ]
    filter_horizontal = ['tags']
    list_display = ['title', 'date_published', 'tags_as_str']
    list_filter = ['date_published', 'tags']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
