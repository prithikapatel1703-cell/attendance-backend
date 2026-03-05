
from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    """Branch/Department (e.g. CSE, EE)."""
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Subject(models.Model):
    """Subject under a department (branch), per year and semester. Each year has 2 semesters."""
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    year = models.CharField(max_length=20, default='1', help_text='Academic year: 1, 2, 3, 4, etc.')
    semester = models.CharField(max_length=20, default='1', help_text='Semester within year: 1 or 2')

    class Meta:
        unique_together = [['code', 'department', 'year', 'semester']]

    def __str__(self):
        return f"{self.code} - {self.name} (Year {self.year}, Sem {self.semester})"


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    full_name = models.CharField(max_length=150, blank=True, null=True)
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    subject = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=10)
    attended_hours = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Number of hours the student attended for this subject/date.',
    )
    total_hours = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Total hours scheduled for this subject/date.',
    )

    def __str__(self):
        return f"{self.student.username} - {self.subject} - {self.date}"
