from django.contrib import admin
from .models import Project, ProjectMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_by", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "role", "joined_at")
    list_filter = ("role",)
    search_fields = ("user__email", "project__name")
