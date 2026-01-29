"""
TeamTrack – Project serializers (create/update, list, detail).
"""
from rest_framework import serializers

from apps.projects.models import Project
from apps.users.models import User


class ProjectCreateUpdateSerializer(serializers.Serializer):
    """Validate project create/update: name, description, status."""

    name = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    status = serializers.ChoiceField(choices=Project.Status.choices, required=False, default=Project.Status.ACTIVE)

    def validate_name(self, value):
        name = (value or "").strip()
        if not name:
            raise serializers.ValidationError("Name cannot be empty.")
        return name


class ProjectListSerializer(serializers.ModelSerializer):
    """Serialize project for list (with creator and optional member count)."""

    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ("id", "name", "description", "status", "created_by", "created_by_email", "member_count", "created_at", "updated_at")
        read_only_fields = fields

    def get_member_count(self, obj):
        return obj.members.count()


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serialize project for detail (with creator and members list)."""

    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ("id", "name", "description", "status", "created_by", "created_by_email", "members", "created_at", "updated_at")
        read_only_fields = fields

    def get_members(self, obj):
        from .member_serializer import ProjectMemberSerializer
        return ProjectMemberSerializer(obj.members.select_related("user").all(), many=True).data
