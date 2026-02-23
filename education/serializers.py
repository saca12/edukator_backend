from rest_framework import serializers

from .models import Grade, Subject, Chapter, Lesson, LessonContent


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["id", "name", "level"]


class SubjectSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True)

    class Meta:
        model = Subject
        fields = ["id", "name", "icon_url", "grade"]


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "title", "order_index", "subject"]


class LessonContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContent
        fields = [
            "id",
            "rich_text_content",
            "illustrations_url",
            "audio_url",
        ]


class LessonSerializer(serializers.ModelSerializer):
    content = LessonContentSerializer(read_only=True)
    chapter_title = serializers.CharField(source="chapter.title", read_only=True)
    subject_id = serializers.UUIDField(source="chapter.subject.id", read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "order_index",
            "is_completed",
            "chapter",
            "chapter_title",
            "subject_id",
            "content",
        ]

