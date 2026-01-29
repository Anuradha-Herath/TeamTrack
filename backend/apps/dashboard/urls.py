"""
TeamTrack – Dashboard URL configuration.
Mounted at /api/v1/dashboard/
"""
from django.urls import path

from apps.dashboard.views.dashboard_views import DashboardSummaryView

urlpatterns = [
    path("summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
]
