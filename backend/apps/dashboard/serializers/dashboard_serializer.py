"""
TeamTrack – Dashboard serializers (output DTOs only).
Read-only; used to serialize dashboard summary from service.
"""
from rest_framework import serializers


class ProjectProgressSerializer(serializers.Serializer):
    """Per-project stats for dashboard summary."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    total_tasks = serializers.IntegerField(read_only=True)
    completed_tasks = serializers.IntegerField(read_only=True)
    pending_tasks = serializers.IntegerField(read_only=True)
    progress_pct = serializers.FloatField(read_only=True)


class DashboardSummarySerializer(serializers.Serializer):
    """Dashboard summary response: totals + progress per project."""

    total_tasks = serializers.IntegerField(read_only=True)
    completed_tasks = serializers.IntegerField(read_only=True)
    pending_tasks = serializers.IntegerField(read_only=True)
    projects = ProjectProgressSerializer(many=True, read_only=True)
