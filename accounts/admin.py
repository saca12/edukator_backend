from django.contrib import admin

from .models import Student, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_staff", "created_at")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email",)
    ordering = ("-created_at",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "user", "current_grade", "created_at")
    list_filter = ("current_grade",)
    search_fields = ("first_name", "last_name", "user__email")
