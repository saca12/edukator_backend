import uuid

from django.db import models

from accounts.models import Student
from core.models import TimeStampedModel


class Progress(TimeStampedModel):
    """
    Aggregated learning progress of a student for a specific lesson.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="progress_entries",
    )
    lesson = models.ForeignKey(
        "education.Lesson",
        on_delete=models.CASCADE,
        related_name="progress_entries",
    )
    completion_percentage = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "lesson")
        ordering = ["-last_activity"]
        indexes = [
            models.Index(fields=["student", "last_activity"]),
        ]

    def __str__(self) -> str:
        return f"{self.student} - {self.lesson} ({self.completion_percentage}%)"

