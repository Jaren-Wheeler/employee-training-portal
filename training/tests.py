from datetime import date

from django.db import IntegrityError
from django.test import TestCase

from .models import Course, Employee, Enrollment, Session


class TrainingModelTests(TestCase):
    def setUp(self) -> None:
        self.employee = Employee.objects.create(
            full_name="John Smith",
            email="john.smith@example.com",
            department=Employee.Department.IT,
        )
        self.course = Course.objects.create(
            title="Python Basics",
            category=Course.Category.TECHNICAL,
            duration_minutes=120,
        )
        self.session = Session.objects.create(
            course=self.course,
            session_date=date(2026, 4, 10),
            instructor_name="Dr. Lee",
            mode=Session.Mode.ONLINE,
        )

    def test_employee_email_must_be_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                full_name="Jane Smith",
                email="john.smith@example.com",
                department=Employee.Department.HR,
            )

    def test_employee_cannot_enroll_twice_in_same_session(self) -> None:
        Enrollment.objects.create(
            employee=self.employee,
            session=self.session,
            status=Enrollment.Status.ENROLLED,
        )

        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(
                employee=self.employee,
                session=self.session,
                status=Enrollment.Status.COMPLETED,
            )
