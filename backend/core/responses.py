"""
TeamTrack – Unified API response format.
All successful API responses use this structure for consistency.
"""
from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, message=None, status_code=status.HTTP_200_OK):
    """
    Return a unified success response.
    - data: payload (dict, list, or single value)
    - message: optional human-readable message
    - status_code: HTTP status (default 200)
    """
    body = {"success": True}
    if data is not None:
        body["data"] = data
    if message:
        body["message"] = message
    return Response(body, status=status_code)


def error_response(message, code=None, details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Return a unified error response.
    - message: human-readable error message
    - code: optional machine-readable code (e.g. validation_error)
    - details: optional dict (e.g. field errors)
    """
    body = {"success": False, "message": message}
    if code:
        body["code"] = code
    if details is not None:
        body["errors"] = details
    return Response(body, status=status_code)
