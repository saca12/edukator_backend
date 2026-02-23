from django.urls import path

from . import views


urlpatterns = [
    path("ai/explain", views.AIExplainView.as_view(), name="ai-explain"),
    path("ai/analyze-error", views.AIAnalyzeErrorView.as_view(), name="ai-analyze-error"),
    path("ai/generate-exercise", views.AIGenerateExerciseView.as_view(), name="ai-generate-exercise"),
    path("ai/hint", views.AIHintView.as_view(), name="ai-hint"),
]

