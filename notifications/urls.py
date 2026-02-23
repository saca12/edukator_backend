from django.urls import path

from . import views


urlpatterns = [
    # Note: spec maps /api/sync/status under "OFFLINE SYNC",
    # but we reuse notifications' status to report counts.
    path("sync/status", views.NotificationsStatusView.as_view(), name="sync-status"),
]

