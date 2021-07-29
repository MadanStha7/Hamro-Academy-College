from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.faculty import FacultyViewSet


router = routers.DefaultRouter()
router.register("faculty", FacultyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
