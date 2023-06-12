from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'phone', 'uuid', 'is_staff', 'is_active',)
    list_filter = ('email', 'phone', 'is_staff', 'is_active',)
    fieldsets = (
        (
            'Main', {
                'fields': ('email', 'password',)
            }
        ),
        (
            'Additional information', {
                'fields': ('first_name', 'last_name', 'phone', 'gender', 'avatar',)
            }
        ),
        (
            'Permissions', {
                'fields': ('is_staff', 'is_active', 'user_permissions')
            }
        )
    )
    add_fieldsets = (
        (
            'Main', {
                'classes': ('wide',),
                'fields': ('email', 'phone', 'password1', 'password2',)
            }
        ), (
            'permissions', {
                'fields': ('is_staff', 'is_active', 'groups',)
            }
        )
    )
    search_fields = ('email', 'phone',)
    ordering = ('-updated_at', '-created_at', 'email', 'phone',)
