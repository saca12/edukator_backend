"""
Business logic for exercise handling, auto-correction and recommendations.
"""

from __future__ import annotations

from typing import Any

from accounts.models import Student
from .models import Exercise, Question, Answer, UserAnswer, ExerciseType


def auto_correct_answer(user_answer: UserAnswer) -> bool:
    """
    Apply auto-correction rules based on exercise type.
    """

    question = user_answer.question
    exercise_type = question.exercise.type.name

    if exercise_type == ExerciseType.QCM:
        if not user_answer.answer:
            return False
        user_answer.is_correct_submission = bool(user_answer.answer.is_correct_option)
    elif exercise_type == ExerciseType.TRUE_FALSE:
        if not user_answer.answer:
            return False
        user_answer.is_correct_submission = bool(user_answer.answer.is_correct_option)
    else:  # TEXT
        # For TEXT we simulate correctness by a simple heuristic
        user_answer.is_correct_submission = bool(user_answer.response_text.strip())

    user_answer.save(update_fields=["is_correct_submission"])
    return user_answer.is_correct_submission


def submit_answers(
    student: Student,
    exercise: Exercise,
    answers_payload: list[dict[str, Any]],
) -> list[UserAnswer]:
    """
    Persist user answers and auto-correct them.
    """

    created_answers: list[UserAnswer] = []
    for item in answers_payload:
        question_id = item.get("question_id")
        answer_id = item.get("answer_id")
        response_text = item.get("response_text", "")

        question = Question.objects.get(id=question_id, exercise=exercise)
        answer = None
        if answer_id:
            answer = Answer.objects.get(id=answer_id, question=question)

        user_answer = UserAnswer.objects.create(
            student=student,
            question=question,
            answer=answer,
            response_text=response_text,
        )
        auto_correct_answer(user_answer)
        created_answers.append(user_answer)

    return created_answers


def compute_exercise_score(exercise: Exercise, student: Student) -> dict[str, Any]:
    """
    Compute the score for a given exercise and student.
    """

    questions = exercise.questions.all()
    total_points = sum(q.points for q in questions)
    earned_points = 0.0

    for question in questions:
        if UserAnswer.objects.filter(
            student=student, question=question, is_correct_submission=True
        ).exists():
            earned_points += question.points

    percentage = (earned_points / total_points * 100) if total_points else 0.0

    return {
        "exercise_id": str(exercise.id),
        "earned_points": earned_points,
        "total_points": total_points,
        "percentage": percentage,
    }


def get_recommended_exercises(student: Student, limit: int = 5) -> list[Exercise]:
    """
    Mock recommendation based on difficulty and recent activity.
    Currently returns latest exercises ordered by difficulty.
    """

    return list(
        Exercise.objects.select_related("difficulty")
        .order_by("difficulty__value", "-created_at")[:limit]
    )

