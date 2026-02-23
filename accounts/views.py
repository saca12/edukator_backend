from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from core.permissions import IsAuthenticatedOrCreate
from .serializers import (
    RegistrationSerializer,
    StudentSerializer,
    UserSerializer,
    UserProfileUpdateSerializer,
)
from .services import authenticate_user, generate_tokens_for_user, get_or_create_student_for_user

User = get_user_model()


class RegisterView(APIView):
    """
    POST /api/auth/register
    """

    permission_classes = [IsAuthenticatedOrCreate]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = generate_tokens_for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "access": tokens.access,
                "refresh": tokens.refresh,
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    """
    POST /api/auth/logout
    Blacklist the refresh token on logout.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                # For simplicity we ignore errors in blacklist step
                pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserView(APIView):
    """
    GET /api/auth/me
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        student = get_or_create_student_for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "student": StudentSerializer(student).data,
            }
        )


class UserProfileView(APIView):
    """
    GET /api/users/profile
    PUT /api/users/profile
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        student = get_or_create_student_for_user(request.user)
        serializer = UserProfileUpdateSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(StudentSerializer(student).data)


class UserProgressView(APIView):
    """
    GET /api/users/progress
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Aggregated user progress is provided by the `progress` app.
        from progress.services import get_student_progress_overview

        student = get_or_create_student_for_user(request.user)
        data = get_student_progress_overview(student)
        return Response(data)


class UserHistoryView(APIView):
    """
    GET /api/users/history
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        from progress.services import get_student_activity_history

        student = get_or_create_student_for_user(request.user)
        data = get_student_activity_history(student)
        return Response(data)

