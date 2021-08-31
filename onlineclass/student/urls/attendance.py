from django.urls import path
from onlineclass.student.views.attendance import StudentOnlineAttendanceView

urlpatterns = [path("online_attendance/", StudentOnlineAttendanceView.as_view())]
