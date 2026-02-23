from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts.services import get_or_create_student_for_user
from .models import Exercise, UserAnswer
from .serializers import ExerciseSerializer, UserAnswerSerializer
from .services import submit_answers, compute_exercise_score, get_recommended_exercises


class ExerciseListView(generics.ListAPIView):
    """
    GET /api/exercises
    """

    queryset = Exercise.objects.select_related("difficulty", "type").all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExerciseDetailView(generics.RetrieveAPIView):
    """
    GET /api/exercises/{id}
    """

    queryset = Exercise.objects.select_related("difficulty", "type").all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExerciseSubmitView(generics.GenericAPIView):
    """
    POST /api/exercises/{id}/submit
    """

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        exercise = self.get_object()
        student = get_or_create_student_for_user(request.user)
        answers_payload = request.data.get("answers", [])
        user_answers = submit_answers(student, exercise, answers_payload)
        serializer = UserAnswerSerializer(user_answers, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExerciseCorrectionView(generics.GenericAPIView):
    """
    GET /api/exercises/{id}/correction
    """

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        exercise = self.get_object()
        student = get_or_create_student_for_user(request.user)
        score_data = compute_exercise_score(exercise, student)
        return Response(score_data)


class ExerciseRecommendedView(generics.GenericAPIView):
    """
    GET /api/exercises/recommended
    """

    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        exercises = get_recommended_exercises(student)
        serializer = self.get_serializer(exercises, many=True)
        return Response(serializer.data)

from django.shortcuts import render

from django.db.models import Max
from .models import UserAnswer, Exercise
from .services import compute_exercise_score

class MyGradesView(generics.GenericAPIView):
    """
    GET /api/exercises/my-grades
    Retourne l'historique des notes de l'élève connecté.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        
        # 1. Récupérer les IDs des exercices que l'élève a complétés
        answered_exercise_ids = UserAnswer.objects.filter(
            student=student
        ).values_list('question__exercise_id', flat=True).distinct()
        
        exercises = Exercise.objects.filter(id__in=answered_exercise_ids).select_related('lesson')
        
        grades = []
        for ex in exercises:
            # 2. Utiliser ton service existant pour calculer le score
            score_data = compute_exercise_score(ex, student)
            
            # 3. Trouver la date de la dernière soumission pour cet exercice
            last_submission = UserAnswer.objects.filter(
                student=student, question__exercise=ex
            ).aggregate(Max('submission_date'))['submission_date__max']

            grades.append({
                "id": score_data["exercise_id"],
                "title": ex.title,
                # On essaie de récupérer la matière de la leçon, sinon on met "Général"
                "subject": ex.lesson.subject.name if hasattr(ex, 'lesson') and ex.lesson and hasattr(ex.lesson, 'subject') else "Général",
                "date": last_submission.strftime("%d/%m/%Y") if last_submission else ex.created_at.strftime("%d/%m/%Y"),
                "score": score_data["earned_points"],
                "total": score_data["total_points"],
                "percentage": score_data["percentage"]
            })
            
        return Response(grades)