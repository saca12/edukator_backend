from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services import get_or_create_student_for_user
from education.models import Lesson
from progress.services import get_revision_needed_lessons
from .models import RevisionSession
from .serializers import RevisionSessionSerializer


class RevisionSessionCreateView(APIView):
    """
    POST /api/revision/session
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        session = RevisionSession.objects.create(student=student)
        # Attach lessons needing revision (mock: tracked for documentation only)
        lessons: list[Lesson] = get_revision_needed_lessons(student)
        payload = {
            "session": RevisionSessionSerializer(session).data,
            "lessons": [
                {"id": str(lesson.id), "title": lesson.title} for lesson in lessons
            ],
        }
        return Response(payload, status=status.HTTP_201_CREATED)

from django.shortcuts import render

# Create your views here.
