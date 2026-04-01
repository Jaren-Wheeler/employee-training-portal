from django.contrib import admin

from .models import Course, Employee, Enrollment, Session


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "department")
    list_filter = ("department",)
    search_fields = ("full_name", "email")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "duration_minutes")
    list_filter = ("category",)
    search_fields = ("title",)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("course", "session_date", "instructor_name", "mode")
    list_filter = ("mode", "session_date", "course__category")
    search_fields = ("course__title", "instructor_name")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("employee", "session", "status")
    list_filter = ("status", "session__course__category", "employee__department")
    search_fields = (
        "employee__full_name",
        "employee__email",
        "session__course__title",
    )
