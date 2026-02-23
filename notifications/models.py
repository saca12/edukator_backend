import uuid

from django.db import models

from accounts.models import Student
from core.models import TimeStampedModel


class Achievement(TimeStampedModel):
    """
    Gamification badge earned by a student.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="achievements",
    )
    badge_name = models.CharField(max_length=150)
    icon_url = models.URLField(blank=True)
    date_earned = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_earned"]

    def __str__(self) -> str:
        return f"{self.badge_name} for {self.student}"


class Notification(TimeStampedModel):
    """
    Notification sent to a student.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Notification to {self.student_id}"

