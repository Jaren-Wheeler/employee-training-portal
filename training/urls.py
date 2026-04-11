from django.urls import path

from . import views


app_name = "training"

urlpatterns = [
    path("", views.home, name="home"),
    path("enrollments/", views.enrollment_list, name="enrollment_list"),
    path("enrollments/create", views.create_enrollment, name="create_enrollments"),
    path("courses/", views.courses_list, name="courses_list"),
    path("courses/create", views.create_courses, name="create_courses.html")
]