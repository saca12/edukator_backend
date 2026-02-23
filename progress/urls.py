from django.urls import path

from . import views


urlpatterns = [
    path("progress/dashboard", views.ProgressDashboardView.as_view(), name="progress-dashboard"),
    path("progress/by-subject", views.ProgressBySubjectView.as_view(), name="progress-by-subject"),
    path("revision/needed", views.RevisionNeededView.as_view(), name="revision-needed"),
]

