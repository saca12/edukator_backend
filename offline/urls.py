from django.urls import path

from . import views


urlpatterns = [
    path("sync/download", views.SyncDownloadView.as_view(), name="sync-download"),
    path("sync/upload", views.SyncUploadView.as_view(), name="sync-upload"),
    path("sync/status", views.SyncStatusView.as_view(), name="sync-status-offline"),
]

