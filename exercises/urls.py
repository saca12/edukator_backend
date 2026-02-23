from django.urls import path

from . import views


urlpatterns = [
    path("exercises", views.ExerciseListView.as_view(), name="exercises-list"),
    path("exercises/<uuid:pk>", views.ExerciseDetailView.as_view(), name="exercises-detail"),
    path("exercises/my-grades", views.MyGradesView.as_view(), name="exercises-my-grades"),
    path(
        "exercises/<uuid:pk>/submit",
        views.ExerciseSubmitView.as_view(),
        name="exercises-submit",
    ),
    path(
        "exercises/<uuid:pk>/correction",
        views.ExerciseCorrectionView.as_view(),
        name="exercises-correction",
    ),
    path(
        "exercises/recommended",
        views.ExerciseRecommendedView.as_view(),
        name="exercises-recommended",
    ),
]

