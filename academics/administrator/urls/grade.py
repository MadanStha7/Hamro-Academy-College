from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.grade import GradeViewSet


router = routers.DefaultRouter()
router.register("grade", GradeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
