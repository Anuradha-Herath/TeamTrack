"""
TeamTrack – Custom middleware.
Request logging: request_id, user, path, method, status.
Do not log secrets or full tokens.
"""
import logging
import uuid

logger = logging.getLogger("core.middleware")


class RequestLoggingMiddleware:
    """
    Log each request with request_id, user (id only), path, method.
    Log response with status after request is processed.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = getattr(request, "request_id", None) or str(uuid.uuid4())[:8]
        request.request_id = request_id

        user_id = None
        if hasattr(request, "user") and request.user.is_authenticated:
            user_id = getattr(request.user, "id", None)

        logger.info(
            "request_id=%s user_id=%s path=%s method=%s",
            request_id,
            user_id,
            request.path,
            request.method,
            extra={
                "request_id": request_id,
                "user": user_id,
                "path": request.path,
                "method": request.method,
            },
        )

        response = self.get_response(request)

        status = getattr(response, "status_code", None)
        logger.info(
            "request_id=%s status=%s",
            request_id,
            status,
            extra={"request_id": request_id, "status": status},
        )

        return response
