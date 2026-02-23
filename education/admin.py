from django.contrib import admin

from .models import Grade, Subject, Chapter, Lesson, LessonContent


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "created_at")
    list_filter = ("level",)
    search_fields = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "grade", "created_at")
    list_filter = ("grade",)
    search_fields = ("name",)


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "order_index")
    list_filter = ("subject",)
    ordering = ("subject", "order_index")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter", "order_index", "is_completed")
    list_filter = ("chapter", "is_completed")
    ordering = ("chapter", "order_index")


@admin.register(LessonContent)
class LessonContentAdmin(admin.ModelAdmin):
    list_display = ("lesson", "created_at")
