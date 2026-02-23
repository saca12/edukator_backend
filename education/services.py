"""
Service layer for pedagogical structure (subjects, chapters, lessons).
"""

from __future__ import annotations

from typing import Any

from accounts.models import Student
from .models import Lesson


def get_related_lessons(lesson: Lesson, limit: int = 5) -> list[Lesson]:
    """
    Return lessons related to the given one inside the same chapter.
    """

    qs = (
        Lesson.objects.filter(chapter=lesson.chapter)
        .exclude(id=lesson.id)
        .order_by("order_index")[:limit]
    )
    return list(qs)


def mark_lesson_completed(student: Student, lesson: Lesson) -> dict[str, Any]:
    """
    Mark a lesson as completed for a given student and update progress.
    """

    from progress.services import update_lesson_progress

    progress = update_lesson_progress(student, lesson, completion_percentage=100)
    lesson.is_completed = True
    lesson.save(update_fields=["is_completed"])

    return {
        "lesson_id": str(lesson.id),
        "completion_percentage": progress.completion_percentage,
        "average_score": progress.average_score,
    }

