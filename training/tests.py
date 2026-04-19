from datetime import date

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

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


class EnrollmentListViewTests(TestCase):
    def setUp(self) -> None:
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
        self.it_employee = Employee.objects.create(
            full_name="John Smith",
            email="john.smith@example.com",
            department=Employee.Department.IT,
        )
        self.hr_employee = Employee.objects.create(
            full_name="Jane Doe",
            email="jane.doe@example.com",
            department=Employee.Department.HR,
        )
        self.sales_employee = Employee.objects.create(
            full_name="Sam Carter",
            email="sam.carter@example.com",
            department=Employee.Department.SALES,
        )
        self.it_enrollment = Enrollment.objects.create(
            employee=self.it_employee,
            session=self.session,
            status=Enrollment.Status.ENROLLED,
        )
        self.hr_enrollment = Enrollment.objects.create(
            employee=self.hr_employee,
            session=self.session,
            status=Enrollment.Status.COMPLETED,
        )
        self.sales_enrollment = Enrollment.objects.create(
            employee=self.sales_employee,
            session=self.session,
            status=Enrollment.Status.ENROLLED,
        )

    def test_enrollment_list_without_filters_returns_all_enrollments(self) -> None:
        response = self.client.get(reverse("training:enrollment_list"))

        enrollments = list(response.context["enrollments"])

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            enrollments,
            [self.it_enrollment, self.hr_enrollment, self.sales_enrollment],
        )
        self.assertIsNone(response.context["selected_status"])
        self.assertIsNone(response.context["selected_department"])

    def test_enrollment_list_filters_by_department(self) -> None:
        response = self.client.get(
            reverse("training:enrollment_list"),
            {"department": Employee.Department.IT},
        )

        enrollments = list(response.context["enrollments"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(enrollments, [self.it_enrollment])
        self.assertEqual(response.context["selected_department"], Employee.Department.IT)
        self.assertIsNone(response.context["selected_status"])

    def test_enrollment_list_filters_by_status(self) -> None:
        response = self.client.get(
            reverse("training:enrollment_list"),
            {"status": Enrollment.Status.COMPLETED},
        )

        enrollments = list(response.context["enrollments"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(enrollments, [self.hr_enrollment])
        self.assertEqual(response.context["selected_status"], Enrollment.Status.COMPLETED)
        self.assertIsNone(response.context["selected_department"])

    def test_enrollment_list_combines_status_and_department_filters(self) -> None:
        response = self.client.get(
            reverse("training:enrollment_list"),
            {
                "status": Enrollment.Status.ENROLLED,
                "department": Employee.Department.HR,
            },
        )

        enrollments = list(response.context["enrollments"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(enrollments, [])
        self.assertEqual(response.context["selected_status"], Enrollment.Status.ENROLLED)
        self.assertEqual(response.context["selected_department"], Employee.Department.HR)
