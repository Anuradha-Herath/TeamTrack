"""
TeamTrack – Project member views (list members, add, remove).
Request handling only; business logic in ProjectService.
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.responses import success_response
from core.exceptions import ValidationError as APIValidationError

from apps.projects.serializers import ProjectMemberSerializer, AddProjectMemberSerializer
from apps.projects.services import ProjectService
from apps.projects.permissions import IsAdminOrProjectOwner


class ProjectMemberListView(APIView):
    """GET /api/v1/projects/<id>/members/ – list members. POST – add member."""
    permission_classes = [IsAuthenticated, IsAdminOrProjectOwner]

    def get_object(self):
        project = ProjectService.get_project_by_id(self.kwargs["pk"], self.request.user)
        self.check_object_permissions(self.request, project)
        return project

    def get(self, request: Request, pk: int) -> Response:
        project = self.get_object()
        members = ProjectService.list_members(project)
        serializer = ProjectMemberSerializer(members, many=True)
        return success_response(data=serializer.data)

    def post(self, request: Request, pk: int) -> Response:
        project = self.get_object()
        serializer = AddProjectMemberSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIValidationError(
                message="Validation failed",
                code="validation_error",
                details=serializer.errors,
            )
        data = serializer.validated_data
        member = ProjectService.add_member(
            project,
            user_id=data["user_id"],
            role=data.get("role", "MEMBER"),
            added_by=request.user,
        )
        return success_response(
            data=ProjectMemberSerializer(member).data,
            status_code=status.HTTP_201_CREATED,
        )


class ProjectMemberDetailView(APIView):
    """DELETE /api/v1/projects/<id>/members/<user_id>/ – remove member."""
    permission_classes = [IsAuthenticated, IsAdminOrProjectOwner]

    def get_object(self):
        project = ProjectService.get_project_by_id(self.kwargs["pk"], self.request.user)
        self.check_object_permissions(self.request, project)
        return project

    def delete(self, request: Request, pk: int, user_id: int) -> Response:
        project = self.get_object()
        ProjectService.remove_member(project, user_id, removed_by=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
