"""
TeamTrack – Projects URL configuration.
Mounted at /api/v1/projects/
"""
from django.urls import path

from apps.projects.views.project_views import ProjectListView, ProjectDetailView
from apps.projects.views.member_views import ProjectMemberListView, ProjectMemberDetailView

urlpatterns = [
    path("", ProjectListView.as_view(), name="projects-list"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="projects-detail"),
    path("<int:pk>/members/", ProjectMemberListView.as_view(), name="projects-members-list"),
    path("<int:pk>/members/<int:user_id>/", ProjectMemberDetailView.as_view(), name="projects-members-detail"),
]
