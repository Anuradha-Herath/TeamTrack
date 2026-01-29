"""
TeamTrack – User views (me + admin list/detail).
Request handling only; business logic in UserService.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from core.responses import success_response
from core.exceptions import ValidationError as APIValidationError
from core.permissions import IsAdminUser

from apps.users.serializers import (
    UserProfileSerializer,
    UserListSerializer,
    UserAdminUpdateSerializer,
)
from apps.users.services import UserService


class MeView(APIView):
    """GET /api/v1/users/me/ – current user profile. PATCH – update profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = UserProfileSerializer(request.user)
        return success_response(data=serializer.data)

    def patch(self, request: Request) -> Response:
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            raise APIValidationError(
                message="Validation failed",
                code="validation_error",
                details=serializer.errors,
            )
        serializer.save()
        return success_response(data=serializer.data)


class UserListView(ListAPIView):
    """GET /api/v1/users/ – admin list all users (paginated, optional filters)."""
    permission_classes = [IsAdminUser]
    serializer_class = UserListSerializer

    def get_queryset(self):
        role = self.request.query_params.get("role")
        is_active_param = self.request.query_params.get("is_active")
        is_active = None
        if is_active_param is not None:
            is_active = str(is_active_param).lower() in ("true", "1", "yes")
        return UserService.list_users(role=role, is_active=is_active)


class UserDetailView(APIView):
    """GET /api/v1/users/<id>/ – admin retrieve. PATCH – admin update role/is_active."""
    permission_classes = [IsAdminUser]

    def get(self, request: Request, pk: int) -> Response:
        user = UserService.get_user_by_id(pk)
        serializer = UserListSerializer(user)
        return success_response(data=serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        serializer = UserAdminUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            raise APIValidationError(
                message="Validation failed",
                code="validation_error",
                details=serializer.errors,
            )
        data = serializer.validated_data
        user = UserService.update_user_role_and_active(
            request.user,
            pk,
            role=data.get("role"),
            is_active=data.get("is_active"),
        )
        return success_response(data=UserListSerializer(user).data)
