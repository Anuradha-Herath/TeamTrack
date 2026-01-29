"""
TeamTrack – Task service.
Business logic for task CRUD and filtering.
Project access is enforced by the view (ProjectService.get_project_by_id); modify by ProjectService.can_modify_project.
"""
from django.db.models import QuerySet
from django.db.models import Q

from core.exceptions import NotFoundError, PermissionDeniedError

from apps.users.models import User
from apps.projects.models import Project, ProjectMember
from apps.projects.services import ProjectService
from apps.tasks.models import Task


class TaskService:
    """Task business logic."""

    @staticmethod
    def list_tasks(
        project: Project,
        status=None,
        assigned_to=None,
        priority=None,
        due_date_from=None,
        due_date_to=None,
        search=None,
    ) -> QuerySet:
        """
        Return tasks for the project with optional filters.
        Ordered by -updated_at.
        """
        qs = Task.objects.filter(project=project).select_related("assigned_to", "created_by").order_by("-updated_at")
        if status is not None:
            qs = qs.filter(status=status)
        if assigned_to is not None:
            qs = qs.filter(assigned_to_id=assigned_to)
        if priority is not None:
            qs = qs.filter(priority=priority)
        if due_date_from is not None:
            qs = qs.filter(due_date__gte=due_date_from)
        if due_date_to is not None:
            qs = qs.filter(due_date__lte=due_date_to)
        if search and search.strip():
            term = search.strip()
            qs = qs.filter(Q(title__icontains=term) | Q(description__icontains=term))
        return qs

    @staticmethod
    def get_task_by_id(project_id: int, task_id: int) -> Task:
        """Return task by id; must belong to project. Raises NotFoundError if not found."""
        try:
            task = Task.objects.select_related("project", "assigned_to", "created_by").get(
                pk=task_id, project_id=project_id
            )
        except Task.DoesNotExist:
            raise NotFoundError(message="Task not found.")
        return task

    @staticmethod
    def create_task(project: Project, user: User, validated_data: dict) -> Task:
        """
        Create task under project. assigned_to must be project member if set.
        Caller must have been checked for modify permission.
        """
        assigned_to_id = validated_data.get("assigned_to")
        if assigned_to_id is not None:
            if not ProjectMember.objects.filter(project=project, user_id=assigned_to_id).exists():
                raise PermissionDeniedError(
                    message="Assigned user must be a member of the project.",
                    code="assignee_not_member",
                )
        task = Task.objects.create(
            project=project,
            title=validated_data["title"],
            description=validated_data.get("description", ""),
            status=validated_data.get("status", Task.Status.TODO),
            priority=validated_data.get("priority", Task.Priority.MEDIUM),
            due_date=validated_data.get("due_date"),
            assigned_to_id=assigned_to_id,
            created_by=user,
        )
        return task

    @staticmethod
    def update_task(project_id: int, task_id: int, validated_data: dict, project: Project = None) -> Task:
        """
        Update task. assigned_to must be project member if set.
        Caller must have been checked for modify permission.
        """
        task = TaskService.get_task_by_id(project_id, task_id)
        assigned_to_id = validated_data.get("assigned_to")
        if assigned_to_id is not None:
            if not ProjectMember.objects.filter(project=task.project, user_id=assigned_to_id).exists():
                raise PermissionDeniedError(
                    message="Assigned user must be a member of the project.",
                    code="assignee_not_member",
                )
        update_fields = []
        for key in ("title", "description", "status", "priority", "due_date", "assigned_to"):
            if key not in validated_data:
                continue
            if key == "assigned_to":
                task.assigned_to_id = validated_data[key]
                update_fields.append("assigned_to_id")
            else:
                setattr(task, key, validated_data[key])
                update_fields.append(key)
        if update_fields:
            task.save(update_fields=update_fields)
        return task

    @staticmethod
    def delete_task(project_id: int, task_id: int) -> None:
        """Delete task. Caller must have been checked for modify permission."""
        task = TaskService.get_task_by_id(project_id, task_id)
        task.delete()
