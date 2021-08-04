from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.apply_shift import ApplyShiftViewSet


router = routers.DefaultRouter()
router.register("apply_shift", ApplyShiftViewSet)

urlpatterns = [path("", include(router.urls))]
