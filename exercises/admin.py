from django.contrib import admin

from .models import Difficulty, ExerciseType, Exercise, Question, Answer, UserAnswer


@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    list_display = ("level_name", "value", "created_at")
    ordering = ("value",)


@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "exercise", "points")
    list_filter = ("exercise",)
    inlines = [AnswerInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "type", "lesson", "created_at")
    list_filter = ("difficulty", "type", "lesson")
    search_fields = ("title",)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "question",
        "answer",
        "is_correct_submission",
        "submission_date",
    )
    list_filter = ("is_correct_submission", "submission_date")

