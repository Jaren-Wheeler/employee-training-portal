from django.shortcuts import render, redirect
from .models import Enrollment, Employee, Session 

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
        "enrollments": enrollments
    })
 
def create_enrollment(request):
    # If form is submitted (POST request), process the data
    if request.method == "POST":
        employee_id = request.POST.get("employee")
        session_id = request.POST.get("session")
        status = request.POST.get("status")

        # Create a new Enrollment record in the database
        # using the selected employee, session, and status
        Enrollment.objects.create(
            employee_id=employee_id,
            session_id=session_id,
            status=status
        )

        # After saving, redirect user to the enrollment list page
        return redirect("training:enrollment_list")

    # If page is accessed normally (GET request),
    # load employees and sessions to populate dropdowns
    employees = Employee.objects.all()
    sessions = Session.objects.all()

    # Render the form and pass data to template
    return render(request, "training/create_enrollment.html", {
        "employees": employees,
        "sessions": sessions
    })