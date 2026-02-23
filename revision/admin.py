from django.contrib import admin

from .models import RevisionSession


@admin.register(RevisionSession)
class RevisionSessionAdmin(admin.ModelAdmin):
    list_display = ("student", "created_at", "is_completed")

