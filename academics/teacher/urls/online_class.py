from django.urls import path, include
from rest_framework import routers

from academics.teacher.viewsets.online_class import OnlineClassInfoViewSet, TeacherStudentOnlineClassAttendanceView

router = routers.DefaultRouter()
router.register(r"online_class", OnlineClassInfoViewSet)

urlpatterns = [path("", include(router.urls)),
               path("online_class_attendance/", TeacherStudentOnlineClassAttendanceView.as_view())]

