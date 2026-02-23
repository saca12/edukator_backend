from django.contrib import admin

from .models import ErrorAnalysis


@admin.register(ErrorAnalysis)
class ErrorAnalysisAdmin(admin.ModelAdmin):
    list_display = ("user_answer", "generated_at")

