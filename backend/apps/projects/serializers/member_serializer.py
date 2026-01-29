"""
TeamTrack – Project member serializers (list members, add member).
"""
from rest_framework import serializers

from apps.projects.models import ProjectMember
from apps.users.models import User


class ProjectMemberSerializer(serializers.ModelSerializer):
    """Serialize project member for list (user id, email, role, joined_at)."""

    user_id = serializers.IntegerField(source="user.id", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = ProjectMember
        fields = ("id", "user_id", "email", "role", "joined_at")
        read_only_fields = fields


class AddProjectMemberSerializer(serializers.Serializer):
    """Validate add member: user_id, role."""

    user_id = serializers.IntegerField(required=True)
    role = serializers.ChoiceField(choices=ProjectMember.Role.choices, required=False, default=ProjectMember.Role.MEMBER)

    def validate_user_id(self, value):
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError("User not found.")
        return value
