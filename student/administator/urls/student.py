from django.urls import include, path
from rest_framework import routers

from student.administator.viewsets.student import StudentInfoViewSet

router = routers.DefaultRouter()
router.register(r"student_info", StudentInfoViewSet)


urlpatterns = [path("", include(router.urls))]
