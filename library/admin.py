from django.contrib import admin

from library.models import Article, Tag


class ArticleAdmin(admin.ModelAdmin):
    fieldset = [('Article informations', {'fields': [
        'title',
        'author',
        'tags',
        'pub_date',
        'content'
    ]})]
    filter_horizontal = ['tags']
    list_display = [
        'title',
        'author',
        'pub_date',
        'tags_as_str'
    ]
    list_filter = ['author', 'pub_date', 'tags']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
