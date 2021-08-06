from django.urls import include, path
from rest_framework import routers

from student.administator.viewsets.previous_academic import PreviousAcademicViewSet

router = routers.DefaultRouter()
router.register(r"previous_academic", PreviousAcademicViewSet)

urlpatterns = [path("", include(router.urls))]
