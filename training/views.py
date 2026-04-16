from django.shortcuts import get_object_or_404, render, redirect
from .models import Enrollment, Employee, Session, Course
from django.db import IntegrityError
from django.contrib import messages

# Handles creating a new enrollment:
# - Displays form (GET)
# - Processes submission (POST)


# =========================
# Home
# =========================
def home(request):
    return render(request, "training/home.html")


# =========================
# Enrollment Views
# =========================
def enrollment_list(request):
    status = request.GET.get("status")
    
    if status: 
        enrollments = Enrollment.objects.filter(status=status)
    else:
        enrollments = Enrollment.objects.all()
        
    return render(request, "training/enrollments.html", {
        "enrollments": enrollments,
        "selected_status": status
    })
    
# Enrollment Form View
def enrollment_management(request):
    employees = Employee.objects.all()
    sessions = Session.objects.all()
    enrollments = Enrollment.objects.all()

    if request.method == "POST":
        employee_id = request.POST.get("employee")
        session_id = request.POST.get("session")
        status = request.POST.get("status")

        existing = Enrollment.objects.filter(
            employee_id=employee_id,
            session_id=session_id
        ).first()

        if existing:
            return render(request, "training/enrollment_management.html", {
                "employees": employees,
                "sessions": sessions,
                "enrollments": enrollments,
                "error": "This employee is already enrolled in this session."
            })

        Enrollment.objects.create(
            employee_id=employee_id,
            session_id=session_id,
            status=status
        )

        return redirect("training:enrollment_management")

    return render(request, "training/enrollment_management.html", {
        "employees": employees,
        "sessions": sessions,
        "enrollments": enrollments
    })
    
def update_status(request, id):
    if request.method == "POST":
        enrollment = Enrollment.objects.get(id=id)
        new_status = request.POST.get("status")

        enrollment.status = new_status
        enrollment.save()

        messages.success(request, "Status updated")

    return redirect("training:enrollment_management")

def analytics_dashboard(request):
    return render(request, "training/analytics.html")

from django.db.models import Count, Q

def course_popularity(request):
    courses = (
        Enrollment.objects
        .values("session__course__title")
        .annotate(
            total_enrollments=Count("id"),
            completed_count=Count("id", filter=Q(status="COMPLETED"))
        )
    )

    # calculate success rate
    for c in courses:
        total = c["total_enrollments"]
        completed = c["completed_count"]
        c["success_rate"] = round((completed / total) * 100, 1) if total > 0 else 0

    return render(request, "training/course_popularity.html", {
        "courses": courses
    })


# =========================
# Courses Views
# =========================

def courses_list(request):
    category = request.GET.get("category")
    if category: 
        courses = Course.objects.filter(category=category)
    else:
        courses = Course.objects.all()

    return render(request, "training/courses.html", {
        "courses": courses,
        "selected_category": category
    })

def create_courses(request):
        # If form is submitted (POST request), process the data
    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        duration = request.POST.get("duration")

        # Create a new Courses record in the database
        # using the selected title, category, and duration
        Course.objects.create(
            title=title,
            category=category,
            duration_minutes=duration
        )

        # After saving, redirect user to the enrollment list page
        return redirect("training:courses_list")

    # If page is accessed normally (GET request),
    # load courses to populate dropdowns
    courses = Course.objects.all()

    # Render the form and pass data to template
    return render(request, "training/create_courses.html", {
        "courses": courses
    })


def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        course.title = request.POST.get("title")
        course.category = request.POST.get("category")
        course.duration_minutes = request.POST.get("duration")
        course.save()

        return redirect("training:courses_list")

    return render(request, "training/edit_course.html", {
        "course": course
    })


def delete_course(request, course_id):
    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        course.delete()

    return redirect("training:courses_list")