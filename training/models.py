from django.db import models


class Employee(models.Model):
    class Department(models.TextChoices):
        IT = "IT", "IT"
        HR = "HR", "HR"
        SALES = "SALES", "Sales"
        FINANCE = "FINANCE", "Finance"
        OPERATIONS = "OPERATIONS", "Operations"
        MARKETING = "MARKETING", "Marketing"

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=20, choices=Department.choices)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.email})"


class Course(models.Model):
    class Category(models.TextChoices):
        TECHNICAL = "TECHNICAL", "Technical"
        SECURITY = "SECURITY", "Security"
        SOFT_SKILLS = "SOFT_SKILLS", "Soft Skills"
        COMPLIANCE = "COMPLIANCE", "Compliance"
        SAFETY = "SAFETY", "Safety"

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices)
    duration_minutes = models.PositiveIntegerField()

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Session(models.Model):
    class Mode(models.TextChoices):
        ONLINE = "ONLINE", "Online"
        IN_PERSON = "IN_PERSON", "In-Person"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sessions")
    session_date = models.DateField()
    instructor_name = models.CharField(max_length=150)
    mode = models.CharField(max_length=20, choices=Mode.choices)

    class Meta:
        ordering = ["-session_date", "course__title"]

    def __str__(self) -> str:
        return f"{self.course.title} on {self.session_date}"


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ENROLLED = "ENROLLED", "Enrolled"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ENROLLED)

    class Meta:
        ordering = ["employee__full_name", "session__session_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "session"],
                name="unique_employee_session_enrollment",
            )
        ]

    def __str__(self) -> str:
        return f"{self.employee.full_name} - {self.session.course.title} ({self.status})"
