"""
TeamTrack – Users URL configuration.
Mounted at /api/v1/users/
"""
from django.urls import path

from apps.users.views.user_views import MeView, UserListView, UserDetailView

urlpatterns = [
    path("me/", MeView.as_view(), name="users-me"),
    path("<int:pk>/", UserDetailView.as_view(), name="users-detail"),
    path("", UserListView.as_view(), name="users-list"),
]
