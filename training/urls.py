from django.urls import path

from . import views


app_name = "training"

urlpatterns = [
    path("", views.home, name="home"),
    path("enrollments/", views.enrollment_list, name="enrollment_list"),
    path("enrollments/manage/", views.enrollment_management, name="enrollment_management"),
    path("enrollments/update/<int:id>/", views.update_status, name="update_status"),

    path("analytics/", views.analytics_dashboard, name="analytics"),
    path("analytics/course-popularity/", views.course_popularity, name="course_popularity"),

    path("courses/", views.courses_list, name="courses_list"),
    path("courses/create", views.create_courses, name="create_courses.html"),
    path("courses/<int:course_id>/edit", views.edit_course, name="edit_course"),
    path("courses/<int:course_id>/delete", views.delete_course, name="delete_course"),

    path("employees/", views.employees_list, name="employees_list"),
    path("employees/create", views.create_employee, name="create_employee.html"),
    path("employees/<int:employee_id>/edit", views.edit_employee, name="edit_employee"),
    path("employees/<int:employee_id>/delete", views.delete_employee, name="delete_employee")
]