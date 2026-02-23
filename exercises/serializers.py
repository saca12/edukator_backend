from rest_framework import serializers

from accounts.serializers import StudentSerializer
from .models import (
    Difficulty,
    ExerciseType,
    Exercise,
    Question,
    Answer,
    UserAnswer,
)


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = ["id", "level_name", "value"]


class ExerciseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseType
        fields = ["id", "name"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "choice_text", "is_correct_option"]
        extra_kwargs = {"is_correct_option": {"write_only": True}}


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "points", "answers"]


class ExerciseSerializer(serializers.ModelSerializer):
    difficulty = DifficultySerializer(read_only=True)
    type = ExerciseTypeSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = [
            "id",
            "title",
            "instructions",
            "difficulty",
            "type",
            "lesson",
            "questions",
        ]


class UserAnswerSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    question_id = serializers.UUIDField(write_only=True)
    answer_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = UserAnswer
        fields = [
            "id",
            "student",
            "question",
            "answer",
            "question_id",
            "answer_id",
            "response_text",
            "is_correct_submission",
            "submission_date",
        ]
        read_only_fields = ["id", "student", "question", "answer", "is_correct_submission", "submission_date"]

