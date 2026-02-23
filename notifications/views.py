from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services import get_or_create_student_for_user
from .models import Achievement, Notification
from .serializers import AchievementSerializer, NotificationSerializer


class NotificationsStatusView(APIView):
    """
    GET /api/sync/status (reused to indicate notification sync/summary)
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        unread_count = Notification.objects.filter(
            student=student, is_read=False
        ).count()
        return Response({"unread_notifications": unread_count})


class NotificationListView(APIView):
    """
    Helper endpoint (not in spec) if needed by clients.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        notifications = Notification.objects.filter(student=student).order_by(
            "-created_at"
        )
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class AchievementListView(APIView):
    """
    Helper endpoint (not in spec) for listing achievements.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        achievements = Achievement.objects.filter(student=student)
        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data)

from django.shortcuts import render

# Create your views here.
