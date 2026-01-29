"""
TeamTrack – Root URL configuration.
API is versioned under /api/v1/.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.users.urls_auth")),
    path("api/v1/users/", include("apps.users.urls_users")),
    path("api/v1/projects/", include("apps.projects.urls")),
    path("api/v1/dashboard/", include("apps.dashboard.urls")),
]
