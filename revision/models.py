import uuid

from django.db import models

from accounts.models import Student
from core.models import TimeStampedModel


class RevisionSession(TimeStampedModel):
    """
    Revision session grouping exercises/lessons to review.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="revision_sessions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Revision session {self.id} for {self.student}"

from django.db import models

# Create your models here.
