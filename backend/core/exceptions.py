"""
TeamTrack – Custom exception classes.
Services and views raise these; the DRF exception handler maps them to HTTP responses.
Do not put business logic here; only exception definitions.
"""
from rest_framework import status


class BaseAPIException(Exception):
    """Base for all API exceptions. Subclass to define status and default message."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Bad request"
    default_code = "error"

    def __init__(self, message=None, code=None, details=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.details = details  # Optional dict for validation errors

    def __str__(self):
        return self.message


class ValidationError(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Validation error"
    default_code = "validation_error"


class AuthenticationError(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "Authentication failed"
    default_code = "authentication_failed"


class PermissionDeniedError(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = "Permission denied"
    default_code = "permission_denied"


class NotFoundError(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Not found"
    default_code = "not_found"


class ConflictError(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_message = "Conflict"
    default_code = "conflict"
