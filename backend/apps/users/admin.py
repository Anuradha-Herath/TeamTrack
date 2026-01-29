from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "role", "is_staff", "date_joined")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
    filter_horizontal = ()

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal", {"fields": ("first_name", "last_name")}),
        ("Role", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
        ("Personal", {"fields": ("first_name", "last_name")}),
        ("Role", {"fields": ("role",)}),
    )
