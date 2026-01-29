"""
TeamTrack – Auth URL configuration.
Mounted at /api/v1/auth/
"""
from django.urls import path

from apps.users.views.auth_views import RegisterView, LoginView, RefreshView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
]
