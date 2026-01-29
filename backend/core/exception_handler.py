"""
TeamTrack – DRF custom exception handler.
Maps exceptions to unified API response format and proper HTTP status codes.
"""
import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response

from .exceptions import BaseAPIException
from .responses import error_response

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Call DRF's default handler first, then normalize response to our format.
    For BaseAPIException, return unified error response with correct status.
    """
    if isinstance(exc, BaseAPIException):
        return error_response(
            message=exc.message,
            code=exc.code,
            details=exc.details,
            status_code=exc.status_code,
        )

    # Let DRF handle standard exceptions (ValidationError, Authentication, etc.)
    response = exception_handler(exc, context)

    if response is not None:
        # Normalize DRF error response to our format
        code = getattr(exc, "default_code", "error")
        data = response.data
        if isinstance(data, dict) and "detail" in data:
            message = data["detail"]
            if isinstance(message, list):
                message = " ".join(str(m) for m in message)
            details = None
        else:
            message = _extract_message(data)
            details = data if isinstance(data, dict) else None
        return error_response(
            message=str(message),
            code=code,
            details=details,
            status_code=response.status_code,
        )

    # Unhandled exception – log and return 500
    logger.exception("Unhandled exception: %s", exc)
    return error_response(
        message="Internal server error",
        code="server_error",
        status_code=500,
    )


def _extract_message(data):
    """Extract a single message string from DRF error data."""
    if data is None:
        return "Error"
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return " ".join(str(item) for item in data)
    if isinstance(data, dict):
        if "detail" in data:
            d = data["detail"]
            return d if isinstance(d, str) else " ".join(str(v) for v in (d if isinstance(d, list) else [d]))
        # Validation errors: flatten first level
        parts = []
        for k, v in data.items():
            if isinstance(v, list):
                parts.append(f"{k}: {'; '.join(str(x) for x in v)}")
            else:
                parts.append(f"{k}: {v}")
        return " ".join(parts)
    return str(data)
