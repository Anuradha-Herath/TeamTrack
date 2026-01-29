"""
TeamTrack – Dashboard views (summary).
Read-only; request handling only; business logic in DashboardService.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.responses import success_response

from apps.dashboard.serializers import DashboardSummarySerializer
from apps.dashboard.services import DashboardService


class DashboardSummaryView(APIView):
    """GET /api/v1/dashboard/summary/ – totals and progress per project for current user."""
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        summary = DashboardService.get_summary(request.user)
        serializer = DashboardSummarySerializer(instance=summary)
        return success_response(data=serializer.data)
