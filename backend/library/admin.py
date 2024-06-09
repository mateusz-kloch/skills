from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Article, Author, Tag


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


class UserAdminConfig(UserAdmin):
    """
    A custom view of users for an admin.
    """
    model = Author
    search_fields = ('user_name', 'email')
    list_filter = ('user_name', 'email', 'is_active', 'is_staff')
    ordering = ('user_name',)
    list_display = ('user_name', 'email', 'id', 'joined', 'is_active', 'is_staff')
    fieldsets = (
        (None, {
            'fields': ('user_name', 'slug', 'email', 'avatar')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'user_name', 'slug', 'email', 'avatar', 'password1', 'password2', 'is_active', 'is_staff'
            )
        }),
    )


admin.site.register(Article, ArticleAdminConfig)
admin.site.register(Author, UserAdminConfig)
admin.site.register(Tag)
