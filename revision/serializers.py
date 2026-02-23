from rest_framework import serializers

from .models import RevisionSession


class RevisionSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevisionSession
        fields = ["id", "student", "created_at", "is_completed"]
        read_only_fields = ["id", "student", "created_at"]

