from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [
    # Authentication
    path("auth/register", views.RegisterView.as_view(), name="auth-register"),
    path("auth/login", TokenObtainPairView.as_view(), name="auth-login"),
    path("auth/logout", views.LogoutView.as_view(), name="auth-logout"),
    path("auth/refresh-token", TokenRefreshView.as_view(), name="auth-refresh"),
    path("auth/me", views.CurrentUserView.as_view(), name="auth-me"),
    # User profile & progress
    path("users/profile", views.UserProfileView.as_view(), name="user-profile"),
    path("users/progress", views.UserProgressView.as_view(), name="user-progress"),
    path("users/history", views.UserHistoryView.as_view(), name="user-history"),
]

