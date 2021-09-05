from django.urls import include, path
from rest_framework import routers
from fees.administrator.viewsets.fee_setup import FeeSetupViewSet

router = routers.DefaultRouter()
router.register(r"fee_setup", FeeSetupViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
