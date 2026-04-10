from django.shortcuts import render, redirect
from .models import Enrollment, Employee, Session 
from django.db import IntegrityError

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
def create_enrollment(request):
    employees = Employee.objects.all()
    sessions = Session.objects.all()

    if request.method == "POST":
        employee_id = request.POST.get("employee")
        session_id = request.POST.get("session")
        status = request.POST.get("status")

        existing = Enrollment.objects.filter(
            employee_id=employee_id,
            session_id=session_id
        ).first()

        if existing:
            if existing.status == "COMPLETED":
                message = "This employee has already completed this session."
            elif existing.status == "ENROLLED":
                message = "This employee is already enrolled in this session."
            elif existing.status == "CANCELLED":
                message = "This employee already has a cancelled enrollment for this session."
            else:
                message = f"This employee already has a {existing.status.lower()} enrollment for this session."

            return render(request, "training/create_enrollment.html", {
                "employees": employees,
                "sessions": sessions,
                "error": message
            })

        Enrollment.objects.create(
            employee_id=employee_id,
            session_id=session_id,
            status=status
        )

        return redirect("training:enrollment_list")

    return render(request, "training/create_enrollment.html", {
        "employees": employees,
        "sessions": sessions
    })
    
def update_status(request, id):
    if request.method == "POST":
        enrollment = Enrollment.objects.get(id=id)
        new_status = request.POST.get("status")

        enrollment.status = new_status
        enrollment.save()

    return redirect("training:enrollment_list")