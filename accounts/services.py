"""
Service layer for user and authentication related business logic.

Views should remain thin and reuse these helpers.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Student

User = get_user_model()


@dataclass
class AuthTokens:
    access: str
    refresh: str


def generate_tokens_for_user(user: User) -> AuthTokens:
    """
    Generate JWT access and refresh tokens for a user.
    """

    refresh = RefreshToken.for_user(user)
    return AuthTokens(access=str(refresh.access_token), refresh=str(refresh))


def authenticate_user(email: str, password: str) -> User | None:
    """
    Authenticate user using Django's built-in authentication backend.
    """

    return authenticate(email=email, password=password)


def get_or_create_student_for_user(user: User) -> Student:
    """
    Ensure a student profile exists for the user.
    """

    student, _ = Student.objects.get_or_create(
        user=user,
        defaults={
            "first_name": "",
            "last_name": "",
            "date_of_birth": None,
            "created_at": timezone.now(),
        },
    )
    return student

