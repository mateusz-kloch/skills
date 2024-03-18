from django.contrib import admin

from .models import Article, Tag


class ArticleAdmin(admin.ModelAdmin):
    fieldset = [
        (
            'Article informations', {
                'fields': [
                    'title',
                    'tags',
                    'pub_date',
                    'content'
                ]
            }
        )
    ]
    filter_horizontal = ['tags']
    list_display = ['title', 'pub_date', 'tags_as_str']
    list_filter = ['pub_date', 'tags']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
