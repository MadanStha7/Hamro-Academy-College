from django.urls import path, include
from rest_framework import routers
from onlineclass.administrator.viewsets.online_class_attendance import (
    StudentOnlineClassAttendanceViewSet,
)


router = routers.DefaultRouter()
router.register("online_class_attendance", StudentOnlineClassAttendanceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
