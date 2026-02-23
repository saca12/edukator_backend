from django.contrib import admin

from .models import Achievement, Notification


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("student", "badge_name", "date_earned")
    list_filter = ("badge_name", "date_earned")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("student", "message", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
