from django.urls import path, include
from rest_framework import routers
from staff.administrator.viewsets.staff import StaffViewSet

router = routers.DefaultRouter()
router.register("staff", StaffViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
