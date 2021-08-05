from django.urls import path, include
from rest_framework import routers
from general.administrator.viewsets.academic_session import AcademicSessionViewSet


router = routers.DefaultRouter()
router.register("academic-session", AcademicSessionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
