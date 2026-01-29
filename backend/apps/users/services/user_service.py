"""
TeamTrack – User service.
Business logic for admin user management: list, get by id, update role and is_active.
"""
from django.db.models import QuerySet

from core.exceptions import NotFoundError, PermissionDeniedError

from apps.users.models import User


class UserService:
    """User management business logic (admin operations)."""

    @staticmethod
    def list_users(role=None, is_active=None) -> QuerySet:
        """
        Return queryset of users, optionally filtered by role and is_active.
        Used by admin list endpoint; ordering by -date_joined.
        """
        qs = User.objects.all().order_by("-date_joined")
        if role is not None:
            qs = qs.filter(role=role)
        if is_active is not None:
            qs = qs.filter(is_active=is_active)
        return qs

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Return user by primary key; raise NotFoundError if not found."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFoundError(message="User not found.")

    @staticmethod
    def update_user_role_and_active(admin_user: User, user_id: int, role=None, is_active=None) -> User:
        """
        Update target user's role and/or is_active. Admin cannot change own role
        or deactivate self (to avoid lockout). Returns updated user.
        """
        user = UserService.get_user_by_id(user_id)

        if user_id == admin_user.pk:
            if role is not None and role != user.role:
                raise PermissionDeniedError(
                    message="You cannot change your own role.",
                    code="cannot_change_own_role",
                )
            if is_active is not None and is_active is False:
                raise PermissionDeniedError(
                    message="You cannot deactivate your own account.",
                    code="cannot_deactivate_self",
                )

        update_fields = []
        if role is not None:
            user.role = role
            update_fields.append("role")
        if is_active is not None:
            user.is_active = is_active
            update_fields.append("is_active")
        if update_fields:
            user.save(update_fields=update_fields)
        return user
