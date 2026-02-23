from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services import get_or_create_student_for_user
from exercises.models import UserAnswer, Exercise
from .serializers import (
    ErrorAnalysisSerializer,
    AIExplainRequestSerializer,
    AIGenerateExerciseRequestSerializer,
    AIHintRequestSerializer,
)
from .services import (
    generate_error_analysis,
    explain_concept,
    generate_mock_exercise,
    generate_hint,
)


class AIExplainView(APIView):
    """
    POST /api/ai/explain
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AIExplainRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = explain_concept(**serializer.validated_data)
        return Response(data)


class AIAnalyzeErrorView(APIView):
    """
    POST /api/ai/analyze-error
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_answer_id = request.data.get("user_answer_id")
        user_answer = UserAnswer.objects.get(
            id=user_answer_id,
            student=get_or_create_student_for_user(request.user),
        )
        analysis = generate_error_analysis(user_answer)
        serializer = ErrorAnalysisSerializer(analysis)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AIGenerateExerciseView(APIView):
    """
    POST /api/ai/generate-exercise
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AIGenerateExerciseRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = generate_mock_exercise(serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED)


class AIHintView(APIView):
    """
    POST /api/ai/hint
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AIHintRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = generate_hint(**serializer.validated_data)
        return Response(data)

from django.shortcuts import render

# Create your views here.
