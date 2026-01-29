"""
TeamTrack – Dashboard service.
Read-only aggregation logic: totals and progress per project for current user's projects.
"""
from django.db.models import Count, Q

from apps.users.models import User
from apps.projects.services import ProjectService
from apps.tasks.models import Task


class DashboardService:
    """Dashboard aggregation logic (read-only)."""

    @staticmethod
    def get_summary(user: User) -> dict:
        """
        Return dashboard summary for the current user:
        - total_tasks, completed_tasks, pending_tasks (across all visible projects)
        - projects: list of { id, name, total_tasks, completed_tasks, pending_tasks, progress_pct }
        """
        projects = ProjectService.list_projects_for_user(user)
        project_ids = list(projects.values_list("id", flat=True))

        if not project_ids:
            return {
                "total_tasks": 0,
                "completed_tasks": 0,
                "pending_tasks": 0,
                "projects": [],
            }

        # Totals across all user's projects
        task_counts = Task.objects.filter(project_id__in=project_ids).aggregate(
            total=Count("id"),
            completed=Count("id", filter=Q(status=Task.Status.DONE)),
            pending=Count("id", filter=Q(status__in=(Task.Status.TODO, Task.Status.IN_PROGRESS))),
        )
        total_tasks = task_counts["total"] or 0
        completed_tasks = task_counts["completed"] or 0
        pending_tasks = task_counts["pending"] or 0

        # Per-project stats
        project_stats = []
        for project in projects:
            proj_tasks = Task.objects.filter(project_id=project.id).aggregate(
                total=Count("id"),
                completed=Count("id", filter=Q(status=Task.Status.DONE)),
                pending=Count("id", filter=Q(status__in=(Task.Status.TODO, Task.Status.IN_PROGRESS))),
            )
            p_total = proj_tasks["total"] or 0
            p_completed = proj_tasks["completed"] or 0
            p_pending = proj_tasks["pending"] or 0
            progress_pct = round((p_completed / p_total * 100), 1) if p_total else 0.0

            project_stats.append({
                "id": project.id,
                "name": project.name,
                "total_tasks": p_total,
                "completed_tasks": p_completed,
                "pending_tasks": p_pending,
                "progress_pct": progress_pct,
            })

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "projects": project_stats,
        }
