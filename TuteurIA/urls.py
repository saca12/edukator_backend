from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # API routes
    path("api/", include("accounts.urls")),
    path("api/", include("education.urls")),
    path("api/", include("exercises.urls")),
    path("api/", include("ai.urls")),
    path("api/", include("progress.urls")),
    path("api/", include("revision.urls")),
    path("api/", include("notifications.urls")),
    path("api/", include("offline.urls")),
]

