"""
TeamTrack – User serializers.
Profile (me), list (admin), and admin update (role / is_active).
"""
from rest_framework import serializers

from apps.users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Serialize user profile for GET/PATCH me."""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role", "date_joined")
        read_only_fields = ("id", "email", "role", "date_joined")


class UserListSerializer(serializers.ModelSerializer):
    """Serialize user for admin list (no sensitive fields)."""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role", "is_active", "date_joined")
        read_only_fields = fields


class UserAdminUpdateSerializer(serializers.Serializer):
    """Validate admin PATCH: role and/or is_active only."""

    role = serializers.ChoiceField(choices=User.Role.choices, required=False)
    is_active = serializers.BooleanField(required=False)

    def validate_role(self, value):
        if value not in (User.Role.ADMIN, User.Role.TEAM_MEMBER):
            raise serializers.ValidationError("Invalid role.")
        return value
