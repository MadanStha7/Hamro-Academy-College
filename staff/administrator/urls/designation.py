from django.urls import path, include
from rest_framework import routers
from staff.administrator.viewsets.designation import DesignationViewSet

router = routers.DefaultRouter()
router.register("designation", DesignationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
