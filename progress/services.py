"""
Service layer for tracking and aggregating learner progress.
"""

from __future__ import annotations

from typing import Any

from accounts.models import Student
from education.models import Lesson, Subject
from exercises.models import Exercise
from .models import Progress


def update_lesson_progress(
    student: Student,
    lesson: Lesson,
    completion_percentage: float | None = None,
    latest_score: float | None = None,
) -> Progress:
    """
    Update or create the Progress object for a (student, lesson) pair.
    """

    progress, _ = Progress.objects.get_or_create(student=student, lesson=lesson)

    if completion_percentage is not None:
        progress.completion_percentage = max(progress.completion_percentage, completion_percentage)

    if latest_score is not None:
        if progress.average_score == 0:
            progress.average_score = latest_score
        else:
            # Simple moving average between existing and latest score
            progress.average_score = (progress.average_score + latest_score) / 2

    progress.save()
    return progress


def get_student_progress_overview(student: Student) -> dict[str, Any]:
    """
    Compute a compact dashboard summary for a student.
    """

    entries = Progress.objects.filter(student=student)
    total_lessons = entries.count()
    avg_completion = (
        sum(e.completion_percentage for e in entries) / total_lessons if total_lessons else 0.0
    )

    return {
        "total_lessons_tracked": total_lessons,
        "average_completion": avg_completion,
    }


def get_student_activity_history(student: Student) -> list[dict[str, Any]]:
    """
    Return a chronological view of lesson activity.
    """

    entries = (
        Progress.objects.filter(student=student)
        .select_related("lesson", "lesson__chapter", "lesson__chapter__subject")
        .order_by("-last_activity")
    )
    history: list[dict[str, Any]] = []
    for e in entries:
        history.append(
            {
                "lesson_id": str(e.lesson_id),
                "lesson_title": e.lesson.title,
                "subject": e.lesson.chapter.subject.name,
                "completion_percentage": e.completion_percentage,
                "average_score": e.average_score,
                "last_activity": e.last_activity,
            }
        )
    return history


def get_progress_dashboard(student: Student) -> dict[str, Any]:
    """
    Aggregated dashboard data (per subject and global).
    """

    entries = (
        Progress.objects.filter(student=student)
        .select_related("lesson", "lesson__chapter", "lesson__chapter__subject")
    )

    by_subject: dict[str, dict[str, Any]] = {}
    for e in entries:
        subject: Subject = e.lesson.chapter.subject
        subject_key = str(subject.id)
        bucket = by_subject.setdefault(
            subject_key,
            {
                "subject_id": subject_key,
                "subject_name": subject.name,
                "lessons_count": 0,
                "avg_completion": 0.0,
            },
        )
        bucket["lessons_count"] += 1
        bucket["avg_completion"] += e.completion_percentage

    for b in by_subject.values():
        if b["lessons_count"]:
            b["avg_completion"] = b["avg_completion"] / b["lessons_count"]

    overview = get_student_progress_overview(student)
    return {
        "overview": overview,
        "by_subject": list(by_subject.values()),
    }


def get_revision_needed_lessons(student: Student) -> list[Lesson]:
    """
    Identify lessons that require revision: low completion or low score.
    """

    return list(
        Lesson.objects.filter(
            progress_entries__student=student,
            progress_entries__completion_percentage__lt=80,
        )
    )

