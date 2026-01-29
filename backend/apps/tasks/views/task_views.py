"""
TeamTrack – Task views (list, create, detail, update, delete).
Request handling only; business logic in TaskService. Project access via ProjectService.
"""
from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from core.responses import success_response
from core.exceptions import ValidationError as APIValidationError
from core.exceptions import PermissionDeniedError

from apps.projects.services import ProjectService
from apps.tasks.serializers import (
    TaskCreateUpdateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
)
from apps.tasks.services import TaskService


class TaskListView(ListAPIView, APIView):
    """GET /api/v1/projects/<project_id>/tasks/ – list (with filters). POST – create (modify permission)."""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskListSerializer

    def get_project(self):
        project_pk = self.kwargs["pk"]
        return ProjectService.get_project_by_id(project_pk, self.request.user)

    def get_queryset(self):
        project = self.get_project()
        params = self.request.query_params
        status_val = params.get("status")
        assigned_to = params.get("assigned_to")
        if assigned_to is not None:
            try:
                assigned_to = int(assigned_to)
            except (ValueError, TypeError):
                assigned_to = None
        priority_val = params.get("priority")
        due_date_from = params.get("due_date_from")
        due_date_to = params.get("due_date_to")
        if due_date_from:
            try:
                due_date_from = datetime.strptime(due_date_from, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                due_date_from = None
        if due_date_to:
            try:
                due_date_to = datetime.strptime(due_date_to, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                due_date_to = None
        search = params.get("search")
        return TaskService.list_tasks(
            project,
            status=status_val,
            assigned_to=assigned_to,
            priority=priority_val,
            due_date_from=due_date_from,
            due_date_to=due_date_to,
            search=search,
        )

    def get(self, request: Request, pk: int) -> Response:
        self.get_project()
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data)

    def post(self, request: Request, pk: int) -> Response:
        project = self.get_project()
        if not ProjectService.can_modify_project(request.user, project):
            raise PermissionDeniedError(message="You do not have permission to create tasks in this project.")
        serializer = TaskCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIValidationError(
                message="Validation failed",
                code="validation_error",
                details=serializer.errors,
            )
        task = TaskService.create_task(project, request.user, serializer.validated_data)
        return success_response(
            data=TaskDetailSerializer(task).data,
            status_code=status.HTTP_201_CREATED,
        )


class TaskDetailView(APIView):
    """GET /api/v1/projects/<project_id>/tasks/<task_id>/ – retrieve. PATCH – update. DELETE – delete (modify permission)."""
    permission_classes = [IsAuthenticated]

    def get_project(self):
        project_pk = self.kwargs["pk"]
        return ProjectService.get_project_by_id(project_pk, self.request.user)

    def get_task(self):
        project_pk = self.kwargs["pk"]
        task_pk = self.kwargs["task_pk"]
        return TaskService.get_task_by_id(project_pk, task_pk)

    def get(self, request: Request, pk: int, task_pk: int) -> Response:
        self.get_project()
        task = self.get_task()
        serializer = TaskDetailSerializer(task)
        return success_response(data=serializer.data)

    def patch(self, request: Request, pk: int, task_pk: int) -> Response:
        project = self.get_project()
        if not ProjectService.can_modify_project(request.user, project):
            raise PermissionDeniedError(message="You do not have permission to update tasks in this project.")
        serializer = TaskCreateUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            raise APIValidationError(
                message="Validation failed",
                code="validation_error",
                details=serializer.errors,
            )
        task = TaskService.update_task(pk, task_pk, serializer.validated_data)
        return success_response(data=TaskDetailSerializer(task).data)

    def delete(self, request: Request, pk: int, task_pk: int) -> Response:
        project = self.get_project()
        if not ProjectService.can_modify_project(request.user, project):
            raise PermissionDeniedError(message="You do not have permission to delete tasks in this project.")
        TaskService.delete_task(pk, task_pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
