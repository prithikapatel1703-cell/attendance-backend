"""
API tests for college attendance backend.
Run: python manage.py test core
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Attendance


class RegisterAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/register/"

    def test_register_student_success(self):
        payload = {
            "username": "student1",
            "email": "student1@test.edu",
            "password": "testpass123",
            "role": "student",
            "full_name": "Test Student",
            "roll_number": "R001",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(email=payload["email"])
        self.assertEqual(user.role, "student")
        self.assertTrue(user.check_password(payload["password"]))

    def test_register_admin_success(self):
        payload = {
            "username": "admin1",
            "email": "admin1@test.edu",
            "password": "adminpass123",
            "role": "admin",
            "full_name": "Test Admin",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload["email"])
        self.assertEqual(user.role, "admin")

    def test_register_duplicate_username_fails(self):
        User.objects.create_user(
            username="existing",
            email="existing@test.edu",
            password="x",
            role="student",
        )
        payload = {
            "username": "existing",
            "email": "new@test.edu",
            "password": "pass123",
            "role": "student",
            "full_name": "New User",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = "/api/login/"
        self.user = User.objects.create_user(
            username="logintest",
            email="login@test.edu",
            password="loginpass123",
            role="admin",
            full_name="Login User",
        )

    def test_login_success(self):
        payload = {
            "email": "login@test.edu",
            "password": "loginpass123",
            "role": "admin",
        }
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["role"], "admin")
        self.assertIn("username", data)

    def test_login_wrong_password_fails(self):
        payload = {
            "email": "login@test.edu",
            "password": "wrongpass",
            "role": "admin",
        }
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.json())

    def test_login_wrong_role_fails(self):
        payload = {
            "email": "login@test.edu",
            "password": "loginpass123",
            "role": "student",
        }
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_email_fails(self):
        payload = {
            "email": "nobody@test.edu",
            "password": "any",
            "role": "admin",
        }
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AttendanceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.attendance_url = "/api/attendance/"
        self.student = User.objects.create_user(
            username="stu",
            email="stu@test.edu",
            password="pass",
            role="student",
        )
        self.faculty = User.objects.create_user(
            username="fac",
            email="fac@test.edu",
            password="pass",
            role="faculty",
        )
        self.admin_user = User.objects.create_user(
            username="adm",
            email="adm@test.edu",
            password="pass",
            role="admin",
        )

    def test_get_attendance_unauthorized_returns_401_or_403(self):
        response = self.client.get(self.attendance_url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_get_attendance_as_student_returns_own_only(self):
        self.client.force_authenticate(user=self.student)
        Attendance.objects.create(student=self.student, subject="Math", date="2025-01-15", status="Present")
        response = self.client.get(self.attendance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        records = data.get("records", data) if isinstance(data, dict) else data
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["student"], self.student.id)

    def test_post_attendance_as_faculty_success(self):
        self.client.force_authenticate(user=self.faculty)
        payload = {
            "student": self.student.id,
            "subject": "Math",
            "date": "2025-01-15",
            "status": "present",
        }
        response = self.client.post(self.attendance_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 1)

    def test_post_attendance_as_student_forbidden(self):
        self.client.force_authenticate(user=self.student)
        payload = {
            "student": self.student.id,
            "subject": "Math",
            "date": "2025-01-15",
            "status": "present",
        }
        response = self.client.post(self.attendance_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
