"""
TeamTrack – Tasks URL configuration.
Mounted at /api/v1/projects/<project_id>/tasks/
"""
from django.urls import path

from apps.tasks.views.task_views import TaskListView, TaskDetailView

urlpatterns = [
    path("", TaskListView.as_view(), name="tasks-list"),
    path("<int:task_pk>/", TaskDetailView.as_view(), name="tasks-detail"),
]
