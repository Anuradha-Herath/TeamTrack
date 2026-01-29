"""
TeamTrack – Task serializers (create/update, list, detail).
"""
from rest_framework import serializers

from apps.tasks.models import Task


class TaskCreateUpdateSerializer(serializers.Serializer):
    """Validate task create/update: title, description, status, priority, due_date, assigned_to."""

    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    status = serializers.ChoiceField(choices=Task.Status.choices, required=False, default=Task.Status.TODO)
    priority = serializers.ChoiceField(choices=Task.Priority.choices, required=False, default=Task.Priority.MEDIUM)
    due_date = serializers.DateField(required=False, allow_null=True)
    assigned_to = serializers.IntegerField(required=False, allow_null=True)

    def validate_title(self, value):
        title = (value or "").strip()
        if not title:
            raise serializers.ValidationError("Title cannot be empty.")
        return title

    def validate_assigned_to(self, value):
        if value is None or value == "":
            return None
        return value


class TaskListSerializer(serializers.ModelSerializer):
    """Serialize task for list (with assignee email)."""

    assigned_to_email = serializers.EmailField(source="assigned_to.email", read_only=True, allow_null=True)
    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "project",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "assigned_to",
            "assigned_to_email",
            "created_by",
            "created_by_email",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class TaskDetailSerializer(serializers.ModelSerializer):
    """Serialize task for detail (same as list; full fields)."""

    assigned_to_email = serializers.EmailField(source="assigned_to.email", read_only=True, allow_null=True)
    created_by_email = serializers.EmailField(source="created_by.email", read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "project",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "assigned_to",
            "assigned_to_email",
            "created_by",
            "created_by_email",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
