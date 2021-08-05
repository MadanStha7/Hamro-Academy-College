from django.urls import path, include
from rest_framework import routers
from staff.administrator.viewsets.staff_academicinfo import StaffAcademicInfoViewSet

router = routers.DefaultRouter()
router.register("staff-academic-info", StaffAcademicInfoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
