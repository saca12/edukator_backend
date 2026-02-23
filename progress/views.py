from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services import get_or_create_student_for_user
from .serializers import ProgressSerializer
from .services import (
    get_progress_dashboard,
    get_revision_needed_lessons,
)
from .models import Progress


class ProgressDashboardView(APIView):
    """
    GET /api/progress/dashboard
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        data = get_progress_dashboard(student)
        return Response(data)


class ProgressBySubjectView(APIView):
    """
    GET /api/progress/by-subject
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        dashboard = get_progress_dashboard(student)
        return Response(dashboard["by_subject"])


class RevisionNeededView(APIView):
    """
    GET /api/revision/needed
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        lessons = get_revision_needed_lessons(student)
        serializer = ProgressSerializer(
            Progress.objects.filter(student=student, lesson__in=lessons),
            many=True,
        )
        return Response(serializer.data)

from django.shortcuts import render

# Create your views here.
