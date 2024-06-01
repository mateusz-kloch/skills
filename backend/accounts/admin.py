from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Author


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
            'fields': ('user_name', 'email')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'user_name', 'email', 'password1', 'password2', 'is_active', 'is_staff'
            )
        }),
    )


admin.site.register(Author, UserAdminConfig)
