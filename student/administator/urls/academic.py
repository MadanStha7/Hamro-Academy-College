from django.urls import include, path
from rest_framework import routers

from student.administator.viewsets.academic import StudentAcademicViewSet


router = routers.DefaultRouter()
router.register(r"student_academic", StudentAcademicViewSet)

urlpatterns = [path("", include(router.urls))]
