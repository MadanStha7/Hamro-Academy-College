from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.shift import ShiftViewSet


router = routers.DefaultRouter()
router.register("shift", ShiftViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
