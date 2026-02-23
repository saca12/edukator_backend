import uuid

from django.db import models

from core.models import TimeStampedModel


class Grade(TimeStampedModel):
    """
    Educational grade (e.g. CM2, 3ème) and level.
    """

    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    LEVEL_CHOICES = [
        (PRIMARY, "Primary"),
        (SECONDARY, "Secondary"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, db_index=True)

    class Meta:
        ordering = ["level", "name"]
        indexes = [
            models.Index(fields=["level"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.level})"


class Subject(TimeStampedModel):
    """
    Academic subject associated with a grade (e.g. Math, History).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    icon_url = models.URLField(blank=True)
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name="subjects",
    )

    class Meta:
        unique_together = ("name", "grade")
        ordering = ["grade__level", "name"]

    def __str__(self) -> str:
        return f"{self.name} - {self.grade.name}"


class Chapter(TimeStampedModel):
    """
    Chapter grouping lessons inside a subject.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    order_index = models.PositiveIntegerField(default=0)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="chapters",
    )

    class Meta:
        ordering = ["subject", "order_index"]
        unique_together = ("subject", "order_index")

    def __str__(self) -> str:
        return f"{self.title} ({self.subject.name})"


class Lesson(TimeStampedModel):
    """
    Lesson belonging to a chapter.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    order_index = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    class Meta:
        ordering = ["chapter", "order_index"]
        unique_together = ("chapter", "order_index")

    def __str__(self) -> str:
        return self.title


class LessonContent(TimeStampedModel):
    """
    Content of a lesson (rich text + optional media).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name="content",
    )
    rich_text_content = models.TextField()
    illustrations_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Lesson Content"
        verbose_name_plural = "Lesson Contents"

    def __str__(self) -> str:
        return f"Content for {self.lesson.title}"

from django.db import models

# Create your models here.
