from rest_framework import serializers

from .models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    subject_name = serializers.CharField(
        source="lesson.chapter.subject.name", read_only=True
    )

    class Meta:
        model = Progress
        fields = [
            "id",
            "lesson",
            "lesson_title",
            "subject_name",
            "completion_percentage",
            "average_score",
            "last_activity",
        ]

