"""
Mock AI services to simulate GPT-4 style explanations and hints.

No external API calls are made; responses are generated deterministically
based on input data so the behaviour is predictable for testing.
"""

from __future__ import annotations

from typing import Any

from exercises.models import UserAnswer, Exercise
from .models import ErrorAnalysis


def generate_error_analysis(user_answer: UserAnswer) -> ErrorAnalysis:
    """
    Create or update an ErrorAnalysis instance for a given user answer.
    """

    explanation = (
        "Votre réponse est correcte. Continuez à appliquer cette logique."
        if user_answer.is_correct_submission
        else "Votre réponse est incorrecte. Revérifiez la définition clé et les exemples."
    )
    hint = (
        "Essayez d'expliquer la solution avec vos propres mots."
        if user_answer.is_correct_submission
        else "Identifiez les mots-clés de la question et relisez la leçon associée."
    )

    analysis, _ = ErrorAnalysis.objects.update_or_create(
        user_answer=user_answer,
        defaults={
            "ai_explanation": explanation,
            "helpful_hint": hint,
        },
    )
    return analysis


def explain_concept(question_text: str, student_answer: str) -> dict[str, Any]:
    """
    Return a mock explanation of a concept.
    """

    return {
        "question": question_text,
        "student_answer": student_answer,
        "explanation": (
            "Analysons la question étape par étape et identifions les éléments clés."
        ),
        "steps": [
            "Repérer les informations importantes dans l'énoncé.",
            "Relier ces informations à la notion étudiée dans la leçon.",
            "Vérifier si la réponse respecte la règle ou la méthode vue en cours.",
        ],
    }


def generate_hint(question_text: str, current_progress: float | None = None) -> dict[str, Any]:
    """
    Return a scaffolded hint adapted to the (mocked) difficulty.
    """

    level = "débutant" if (current_progress or 0) < 50 else "confirmé"
    return {
        "question": question_text,
        "level": level,
        "hint": "Commence par reformuler la question puis cherche un exemple similaire dans la leçon.",
    }


def generate_mock_exercise(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Generate a fake exercise description for testing.
    """

    subject = payload.get("subject")
    grade_level = payload.get("grade_level")
    difficulty = payload.get("difficulty")

    return {
        "title": f"Exercice {difficulty} - {subject} ({grade_level})",
        "instructions": "Lis attentivement chaque question puis choisis la bonne réponse.",
        "questions": [
            {
                "question_text": "Question générée automatiquement n°1.",
                "type": "QCM",
                "choices": [
                    {"text": "Choix A", "is_correct": False},
                    {"text": "Choix B", "is_correct": True},
                ],
            }
        ],
    }


def summarize_exercise_performance(exercise: Exercise, user_answers: list[UserAnswer]) -> dict[str, Any]:
    """
    Provide a high-level AI-style feedback summary for an exercise attempt.
    """

    total = len(user_answers)
    correct = len([ua for ua in user_answers if ua.is_correct_submission])
    return {
        "exercise_id": str(exercise.id),
        "summary": f"Vous avez correctement répondu à {correct} question(s) sur {total}.",
    }

