import uuid

from django.db import models

from core.models import TimeStampedModel


class ErrorAnalysis(TimeStampedModel):
    """
    AI-generated explanation and hint for a specific user answer.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_answer = models.OneToOneField(
        "exercises.UserAnswer",
        on_delete=models.CASCADE,
        related_name="error_analysis",
    )
    ai_explanation = models.TextField()
    helpful_hint = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self) -> str:
        return f"Analysis for answer {self.user_answer_id}"

from django.db import models

# Create your models here.
