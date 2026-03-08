from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "department", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "department")

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("phone", "department")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("phone", "department")}),
    )
