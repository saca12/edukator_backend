from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services import get_or_create_student_for_user
from .models import OfflineContent
from .serializers import OfflineContentSerializer


class SyncDownloadView(APIView):
    """
    POST /api/sync/download
    Register content that should be downloaded for offline usage.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        serializer = OfflineContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = OfflineContent.objects.create(
            student=student,
            **{
                "content_type": serializer.validated_data["content_type"],
                "related_entity_id": serializer.validated_data["related_entity_id"],
                "local_file_path": serializer.validated_data["local_file_path"],
            },
        )
        return Response(
            OfflineContentSerializer(instance).data, status=status.HTTP_201_CREATED
        )


class SyncUploadView(APIView):
    """
    POST /api/sync/upload
    Notify backend that offline progress has been synchronized.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # For this mock implementation, we simply acknowledge the payload.
        return Response({"status": "uploaded"}, status=status.HTTP_200_OK)


class SyncStatusView(APIView):
    """
    GET /api/sync/status
    Return minimal sync information (delegated in practice to notifications).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        count = OfflineContent.objects.filter(student=student).count()
        return Response({"offline_items": count})

from django.shortcuts import render

# Create your views here.
