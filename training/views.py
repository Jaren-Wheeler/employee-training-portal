from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Employee, Enrollment, Session

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
    department = request.GET.get("department")

    enrollments = Enrollment.objects.select_related("employee", "session__course")

    if status:
        enrollments = enrollments.filter(status=status)

    if department:
        enrollments = enrollments.filter(employee__department=department)

    return render(request, "training/enrollments.html", {
        "enrollments": enrollments,
        "selected_status": status,
        "selected_department": department,
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

# =========================
# Employee Views
# =========================

def employees_list(request):
    department = request.GET.get("department")
    if department: 
        employees = Employee.objects.filter(department=department)
    else:
        employees = Employee.objects.all()

    return render(request, "training/employees.html", {
        "employees": employees,
        "selected_department": department
    })

def create_employee(request):
        # If form is submitted (POST request), process the data
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        department = request.POST.get("department")

        # Create a new Employee record in the database
        # using the selected title, category, and duration
        Employee.objects.create(
            full_name=full_name,
            email=email,
            department=department
        )

        # After saving, redirect user to the employee list page
        return redirect("training:employees_list")

    # If page is accessed normally (GET request),
    # load courses to populate dropdowns
    employees = Employee.objects.all()

    # Render the form and pass data to template
    return render(request, "training/create_employee.html", {
        "employees": employees
    })


def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        employee.full_name = request.POST.get("full_name")
        employee.email = request.POST.get("email")
        employee.department = request.POST.get("department")
        employee.save()

        return redirect("training:employees_list")

    return render(request, "training/edit_employees.html", {
        "employee": employee
    })


def delete_employee(request, employee_id):
    if request.method == "POST":
        course = get_object_or_404(Employee, id=employee_id)
        course.delete()

    return redirect("training:employees_list")

# =========================
# Analytics Views
# =========================

def analytics_dashboard(request):
    return render(request, "training/analytics.html")


# -------------------------
# Course Popularity
# -------------------------
def course_popularity(request):
    courses = list(
        Course.objects
        .annotate(
            total_enrollments=Count("sessions__enrollments"),
            completed_enrollments=Count(
                "sessions__enrollments",
                filter=Q(sessions__enrollments__status=Enrollment.Status.COMPLETED),
            ),
        )
        .order_by("-total_enrollments", "title")
    )

    for course in courses:
        total = course.total_enrollments
        completed = course.completed_enrollments
        course.success_rate = round((completed / total) * 100, 1) if total > 0 else 0

    return render(request, "training/course_popularity.html", {
        "courses": courses
    })


# =========================
# Analytics Views
# =========================

def analytics_dashboard(request):
    return render(request, "training/analytics.html")


# -------------------------
# Course Popularity
# -------------------------
def course_popularity(request):
    courses = list(
        Course.objects
        .annotate(
            total_enrollments=Count("sessions__enrollments"),
            completed_enrollments=Count(
                "sessions__enrollments",
                filter=Q(sessions__enrollments__status=Enrollment.Status.COMPLETED),
            ),
        )
        .order_by("-total_enrollments", "title")
    )

    for course in courses:
        total = course.total_enrollments
        completed = course.completed_enrollments
        course.success_rate = round((completed / total) * 100, 1) if total > 0 else 0

    return render(request, "training/course_popularity.html", {
        "courses": courses
    })


# -------------------------
# Department Participation
# -------------------------
def department_participation(request):
    departments = (
        Employee.objects
        .values("department")
        .annotate(
            total_enrollments=Count("enrollments"),
            completed_count=Count(
                "enrollments",
                filter=Q(enrollments__status=Enrollment.Status.COMPLETED)
            )
        )
        .order_by("-completed_count")
    )

    return render(request, "training/department_participation.html", {
        "departments": departments
    })
    
# -------------------------
# Enrollment per Session
# -------------------------
def enrollments_per_session(request):
    sessions = (
        Session.objects
        .annotate(total_enrollments=Count("enrollments"))
        .order_by("-total_enrollments")
    )

    return render(request, "training/enrollments_per_session.html", {
        "sessions": sessions
    })