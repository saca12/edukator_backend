from django.urls import path

from . import views


urlpatterns = [
    path("revision/session", views.RevisionSessionCreateView.as_view(), name="revision-session"),
]

