from django.shortcuts import render, redirect
from .models import Enrollment, Employee, Session 
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