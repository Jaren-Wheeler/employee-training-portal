# Employee Training Session Analytics Portal

This repository contains a Django starter project for the CPRO 2201 final project.

## Included

- Django project scaffold
- `training` app
- Required core models:
  - `Employee`
  - `Course`
  - `Session`
  - `Enrollment`
- Admin registration
- Initial migration
- Basic tests for key model constraints

## Setup

1. Create a virtual environment:

```powershell
py -m venv .venv
```

2. Activate it:

```powershell
.venv\\Scripts\\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run migrations:

```powershell
python manage.py migrate
```

5. Create an admin user:

```powershell
python manage.py createsuperuser
```

6. Start the server:

```powershell
python manage.py runserver
```

## Next Build Steps

- Add CRUD views and templates for Employees, Courses, Sessions, and Enrollments
- Add filtering for department, category, session date/instructor, and enrollment status
- Build the analytics pages required by your group size
- Seed the minimum sample dataset required by the assignment
