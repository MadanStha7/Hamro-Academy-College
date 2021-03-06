from django.urls import path, include
from rest_framework import routers

from academics.teacher.views.online_class import TeacherStudentOnlineClassAttendanceView
from academics.teacher.viewsets.online_class import OnlineClassInfoViewSet

router = routers.DefaultRouter()
router.register(r"teacher/online_class", OnlineClassInfoViewSet)

urlpatterns = [path("", include(router.urls)),
               path("teacher/online_class_attendance/", TeacherStudentOnlineClassAttendanceView.as_view())]

