from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Student

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_staff", "created_at"]
        read_only_fields = ["id", "created_at"]


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_grade_name = serializers.CharField(
        source="current_grade.name", read_only=True
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "date_of_birth",
            "current_grade",
            "current_grade_name",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at", "current_grade_name"]


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer used for user + student registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True, required=False, allow_null=True)
    current_grade = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "date_of_birth",
            "current_grade",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        from education.models import Grade  # imported lazily to avoid circular import

        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        date_of_birth = validated_data.pop("date_of_birth", None)
        current_grade_id = validated_data.pop("current_grade", None)

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )

        current_grade = None
        if current_grade_id:
            current_grade = Grade.objects.filter(id=current_grade_id).first()

        Student.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            current_grade=current_grade,
        )

        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Update serializer for the student profile."""

    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "current_grade",
        ]

