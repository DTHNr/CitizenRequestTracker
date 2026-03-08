from django.contrib import admin
from .models import Category, Request, StatusChange


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "status", "priority", "created_by", "assigned_to", "created_at")
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description", "category__name", "created_by__username")


@admin.register(StatusChange)
class StatusChangeAdmin(admin.ModelAdmin):
    list_display = ("request", "old_status", "new_status", "changed_by", "changed_at")
    list_filter = ("old_status", "new_status")
    readonly_fields = ("request", "old_status", "new_status", "changed_by", "changed_at", "notes")
