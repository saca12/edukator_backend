from django.contrib import admin

from .models import OfflineContent


@admin.register(OfflineContent)
class OfflineContentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "content_type",
        "related_entity_id",
        "local_file_path",
        "last_synced",
    )
    list_filter = ("content_type",)

