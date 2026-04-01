from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("TECHNICAL", "Technical"),
                            ("SECURITY", "Security"),
                            ("SOFT_SKILLS", "Soft Skills"),
                            ("COMPLIANCE", "Compliance"),
                            ("SAFETY", "Safety"),
                        ],
                        max_length=20,
                    ),
                ),
                ("duration_minutes", models.PositiveIntegerField()),
            ],
            options={"ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "department",
                    models.CharField(
                        choices=[
                            ("IT", "IT"),
                            ("HR", "HR"),
                            ("SALES", "Sales"),
                            ("FINANCE", "Finance"),
                            ("OPERATIONS", "Operations"),
                            ("MARKETING", "Marketing"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
            options={"ordering": ["full_name"]},
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_date", models.DateField()),
                ("instructor_name", models.CharField(max_length=150)),
                (
                    "mode",
                    models.CharField(
                        choices=[("ONLINE", "Online"), ("IN_PERSON", "In-Person")],
                        max_length=20,
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="sessions",
                        to="training.course",
                    ),
                ),
            ],
            options={"ordering": ["-session_date", "course__title"]},
        ),
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ENROLLED", "Enrolled"),
                            ("COMPLETED", "Completed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="ENROLLED",
                        max_length=20,
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="enrollments",
                        to="training.employee",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="enrollments",
                        to="training.session",
                    ),
                ),
            ],
            options={"ordering": ["employee__full_name", "session__session_date"]},
        ),
        migrations.AddConstraint(
            model_name="enrollment",
            constraint=models.UniqueConstraint(
                fields=("employee", "session"),
                name="unique_employee_session_enrollment",
            ),
        ),
    ]
