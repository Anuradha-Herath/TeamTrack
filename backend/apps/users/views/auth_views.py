"""
TeamTrack – Auth views (register, login, refresh, logout).
Request handling only; business logic in AuthService; tokens via simplejwt.
"""
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from core.responses import success_response
from core.exceptions import ValidationError as APIValidationError

from apps.users.serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from apps.users.services import AuthService


class RegisterView(APIView):
    """POST /api/v1/auth/register/ – create user and return tokens."""
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIValidationError(
                message="Validation failed",
                code="validation_error",
                details=serializer.errors,
            )
        user = AuthService.register_user(serializer.validated_data)
        tokens = _tokens_for_user(user)
        return success_response(
            data={
                "user": UserProfileSerializer(user).data,
                "access": tokens["access"],
                "refresh": tokens["refresh"],
            },
            status_code=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/v1/auth/login/ – authenticate and return tokens."""
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            raise APIValidationError(
                message="Invalid credentials or validation failed",
                code="validation_error",
                details=serializer.errors,
            )
        user = serializer.validated_data["user"]
        tokens = _tokens_for_user(user)
        return success_response(
            data={
                "user": UserProfileSerializer(user).data,
                "access": tokens["access"],
                "refresh": tokens["refresh"],
            },
        )


class RefreshView(APIView):
    """POST /api/v1/auth/refresh/ – return new access (and optionally refresh) token."""
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = TokenRefreshSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIValidationError(
                message="Invalid or expired refresh token",
                code="invalid_refresh",
                details=serializer.errors,
            )
        data = serializer.validated_data
        return success_response(
            data={
                "access": data["access"],
                "refresh": data.get("refresh"),
            },
        )


class LogoutView(APIView):
    """POST /api/v1/auth/logout/ – blacklist refresh token if provided."""
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # Invalid token: still return success so client can clear storage
        return success_response(data=None, message="Logged out successfully.")


def _tokens_for_user(user):
    """Generate access and refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
