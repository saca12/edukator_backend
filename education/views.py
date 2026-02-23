from rest_framework import generics, permissions
from rest_framework.response import Response

from accounts.services import get_or_create_student_for_user
from .models import Subject, Chapter, Lesson
from .serializers import SubjectSerializer, LessonSerializer, ChapterSerializer
from .services import get_related_lessons, mark_lesson_completed


class SubjectListView(generics.ListAPIView):
    """
    GET /api/subjects
    """

    queryset = Subject.objects.select_related("grade").all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubjectDetailView(generics.RetrieveAPIView):
    """
    GET /api/subjects/{id}
    """

    queryset = Subject.objects.select_related("grade").all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubjectChaptersView(generics.ListAPIView):
    """
    GET /api/subjects/{id}/chapters
    """

    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        subject_id = self.kwargs["pk"]
        return Chapter.objects.filter(subject_id=subject_id).order_by("order_index")


class LessonListView(generics.ListAPIView):
    """
    GET /api/lessons
    """

    queryset = Lesson.objects.select_related("chapter", "chapter__subject").all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonDetailView(generics.RetrieveAPIView):
    """
    GET /api/lessons/{id}
    """

    queryset = Lesson.objects.select_related("chapter", "chapter__subject").all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonRelatedView(generics.GenericAPIView):
    """
    GET /api/lessons/{id}/related
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lesson = self.get_object()
        related_lessons = get_related_lessons(lesson)
        serializer = self.get_serializer(related_lessons, many=True)
        return Response(serializer.data)


class LessonCompleteView(generics.GenericAPIView):
    """
    POST /api/lessons/{id}/complete
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        student = get_or_create_student_for_user(request.user)
        result = mark_lesson_completed(student, lesson)
        return Response(result)

from django.shortcuts import render

# Create your views here.
