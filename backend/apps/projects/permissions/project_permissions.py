"""
TeamTrack – Project permissions.
Only admins or project owners (created_by or PROJECT_ADMIN member) can modify projects and members.
"""
from rest_framework import permissions

from apps.projects.services import ProjectService


class IsAdminOrProjectOwner(permissions.BasePermission):
    """
    Allow read if user has access to the project (enforced by view get_object).
    Allow write (PATCH, DELETE, POST members) only if user is global admin, project creator, or PROJECT_ADMIN member.
    """

    message = "You do not have permission to modify this project."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        from apps.projects.models import Project

        if not isinstance(obj, Project):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True  # Access already enforced by get_object using ProjectService.get_project_by_id
        return ProjectService.can_modify_project(request.user, obj)
