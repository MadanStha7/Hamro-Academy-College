from django.urls import include, path
from rest_framework import routers

from student.administator.viewsets.guardain import GuardianInfoViewSet

router = routers.DefaultRouter()
router.register(r"guardian_info", GuardianInfoViewSet)

urlpatterns = [path("", include(router.urls))]
