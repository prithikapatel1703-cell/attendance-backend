from django.urls import path
from .views import (
    register, login_view, attendance_view,
    user_list_view, user_detail_view,
    department_list_view, department_detail_view,
    subject_list_view, subject_detail_view,
    bulk_student_upload_view, export_attendance_excel_view,
    bulk_attendance_upload_view,
)

urlpatterns = [
    path('register/', register),
    path('login/', login_view),
    path('attendance/', attendance_view),
    path('users/', user_list_view),
    path('users/<int:pk>/', user_detail_view),
    path('departments/', department_list_view),
    path('departments/<int:pk>/', department_detail_view),
    path('subjects/', subject_list_view),
    path('subjects/<int:pk>/', subject_detail_view),
    path('students/bulk-upload/', bulk_student_upload_view),
    path('export/attendance-data/', export_attendance_excel_view),
    path('attendance/bulk-upload/', bulk_attendance_upload_view),
]
