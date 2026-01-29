"""
TeamTrack – Base permission classes.
App-specific permissions (e.g. IsProjectMember) live in apps/<app>/permissions/.
"""
from rest_framework import permissions


class IsAuthenticated(permissions.IsAuthenticated):
    """
    Allow only authenticated users.
    DRF's default; re-exported here for consistency and future overrides.
    """
    pass


class IsAdminUser(permissions.BasePermission):
    """
    Allow only users with role ADMIN.
    Used for system-wide admin endpoints (e.g. list all users).
    """
    message = "Admin access required."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, "role", None) == "ADMIN"


class IsProjectMember(permissions.BasePermission):
    """
    Placeholder for project-level membership check.
    Used later when project/task endpoints are implemented:
    - Resolve project from view kwargs and check request.user is a member.
    """
    message = "You are not a member of this project."

    def has_permission(self, request, view):
        # Default: require authenticated user; object-level check in has_object_permission
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Override in subclasses or in app-specific permissions to check project membership
        return True
