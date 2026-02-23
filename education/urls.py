from django.urls import path

from . import views


urlpatterns = [
    path("subjects", views.SubjectListView.as_view(), name="subjects-list"),
    path("subjects/<uuid:pk>", views.SubjectDetailView.as_view(), name="subjects-detail"),
    path(
        "subjects/<uuid:pk>/chapters",
        views.SubjectChaptersView.as_view(),
        name="subjects-chapters",
    ),
    path("lessons", views.LessonListView.as_view(), name="lessons-list"),
    path("lessons/<uuid:pk>", views.LessonDetailView.as_view(), name="lessons-detail"),
    path(
        "lessons/<uuid:pk>/related",
        views.LessonRelatedView.as_view(),
        name="lessons-related",
    ),
    path(
        "lessons/<uuid:pk>/complete",
        views.LessonCompleteView.as_view(),
        name="lessons-complete",
    ),
]

