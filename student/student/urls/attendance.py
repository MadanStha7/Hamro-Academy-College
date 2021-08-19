from django.urls import path
from student.student.viewsets.attendance import StudentOnlineAttendanceView

urlpatterns = [
    path("student_online_attendance/", StudentOnlineAttendanceView.as_view())
]
