import uuid

from django.db import models

from accounts.models import Student
from core.models import TimeStampedModel


class Difficulty(TimeStampedModel):
    """
    Difficulty level for an exercise (e.g. Easy, Medium).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level_name = models.CharField(max_length=50, unique=True)
    value = models.PositiveSmallIntegerField(help_text="Numerical representation of difficulty")

    class Meta:
        ordering = ["value"]

    def __str__(self) -> str:
        return f"{self.level_name} ({self.value})"


class ExerciseType(TimeStampedModel):
    """
    Exercise type: QCM, TEXT, TRUE_FALSE.
    """

    QCM = "QCM"
    TEXT = "TEXT"
    TRUE_FALSE = "TRUE_FALSE"

    TYPE_CHOICES = [
        (QCM, "Multiple choice"),
        (TEXT, "Free text"),
        (TRUE_FALSE, "True / False"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)

    def __str__(self) -> str:
        return self.name


class Exercise(TimeStampedModel):
    """
    Exercise containing one or more questions.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    difficulty = models.ForeignKey(
        Difficulty,
        on_delete=models.PROTECT,
        related_name="exercises",
    )
    type = models.ForeignKey(
        ExerciseType,
        on_delete=models.PROTECT,
        related_name="exercises",
    )
    lesson = models.ForeignKey(
        "education.Lesson",
        on_delete=models.CASCADE,
        related_name="exercises",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.title


class Question(TimeStampedModel):
    """
    Question inside an exercise.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_text = models.TextField()
    points = models.FloatField(default=1.0)

    def __str__(self) -> str:
        return self.question_text[:50]


class Answer(TimeStampedModel):
    """
    Possible answer choice for a question.
    For QCM multiple choices are allowed with exactly one correct option.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    choice_text = models.CharField(max_length=255)
    is_correct_option = models.BooleanField(default=False)

    class Meta:
        ordering = ["question", "id"]

    def __str__(self) -> str:
        return self.choice_text


class UserAnswer(TimeStampedModel):
    """
    Answer submission by a student.
    Supports:
    - Choice-based answers (FK to `Answer`)
    - Free-text answers (`response_text`) for TEXT exercises
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="user_answers",
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_answers",
    )
    response_text = models.TextField(blank=True)
    is_correct_submission = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submission_date"]
        indexes = [
            models.Index(fields=["student", "submission_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.student} -> {self.question}"

