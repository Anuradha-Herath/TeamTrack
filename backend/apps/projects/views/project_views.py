"""
TeamTrack – Project views (list, create, detail, update, delete).
Request handling only; business logic in ProjectService.
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from core.responses import success_response
from core.exceptions import ValidationError as APIValidationError

from apps.projects.serializers import (
    ProjectCreateUpdateSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
)
from apps.projects.services import ProjectService
from apps.projects.permissions import IsAdminOrProjectOwner as ProjectPermission


class ProjectListView(ListAPIView, APIView):
    """GET /api/v1/projects/ – list projects for current user. POST – create project."""
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return ProjectService.list_projects_for_user(self.request.user)

    def get(self, request: Request) -> Response:
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data)

    def post(self, request: Request) -> Response:
        serializer = ProjectCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIValidationError(
                message="Validation failed",
                code="validation_error",
                details=serializer.errors,
            )
        project = ProjectService.create_project(request.user, serializer.validated_data)
        return success_response(
            data=ProjectDetailSerializer(project).data,
            status_code=status.HTTP_201_CREATED,
        )


class ProjectDetailView(APIView):
    """GET /api/v1/projects/<id>/ – retrieve. PATCH – update. DELETE – delete."""
    permission_classes = [IsAuthenticated, ProjectPermission]

    def get_object(self):
        project = ProjectService.get_project_by_id(self.kwargs["pk"], self.request.user)
        self.check_object_permissions(self.request, project)
        return project

    def get(self, request: Request, pk: int) -> Response:
        project = self.get_object()
        serializer = ProjectDetailSerializer(project)
        return success_response(data=serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        project = self.get_object()
        serializer = ProjectCreateUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            raise APIValidationError(
                message="Validation failed",
                code="validation_error",
                details=serializer.errors,
            )
        project = ProjectService.update_project(pk, serializer.validated_data)
        return success_response(data=ProjectDetailSerializer(project).data)

    def delete(self, request: Request, pk: int) -> Response:
        project = self.get_object()
        ProjectService.delete_project(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
