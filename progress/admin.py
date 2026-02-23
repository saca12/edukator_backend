from django.contrib import admin

from .models import Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "lesson",
        "completion_percentage",
        "average_score",
        "last_activity",
    )
    list_filter = ("student", "lesson")

