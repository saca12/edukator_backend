from rest_framework import serializers

from exercises.serializers import UserAnswerSerializer, ExerciseSerializer
from .models import ErrorAnalysis


class ErrorAnalysisSerializer(serializers.ModelSerializer):
    user_answer = UserAnswerSerializer(read_only=True)

    class Meta:
        model = ErrorAnalysis
        fields = ["id", "user_answer", "ai_explanation", "helpful_hint", "generated_at"]


class AIExplainRequestSerializer(serializers.Serializer):
    question_text = serializers.CharField()
    student_answer = serializers.CharField()


class AIHintRequestSerializer(serializers.Serializer):
    question_text = serializers.CharField()
    current_progress = serializers.FloatField(required=False)


class AIGenerateExerciseRequestSerializer(serializers.Serializer):
    subject = serializers.CharField()
    grade_level = serializers.CharField()
    difficulty = serializers.CharField()


