import uuid

from django.db import models

from accounts.models import Student
from core.models import TimeStampedModel


class OfflineContent(TimeStampedModel):
    """
    Metadata for synchronized offline content.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="offline_contents",
    )
    content_type = models.CharField(max_length=50)
    related_entity_id = models.UUIDField()
    local_file_path = models.CharField(max_length=255)
    last_synced = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["student", "content_type"]),
        ]

    def __str__(self) -> str:
        return f"{self.content_type} ({self.related_entity_id}) for {self.student_id}"

