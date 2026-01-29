from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "priority", "assigned_to", "due_date", "created_by", "updated_at")
    list_filter = ("status", "priority", "project")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
