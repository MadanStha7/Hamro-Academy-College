from django.urls import include, path
from rest_framework import routers
from fees.entrypoints.route_handlers.administrator import (
    FeeSetupViewSet,
    FeeConfigView,
    ActivateDeactivateFeeConfig,
    StudentFeeCollectionView,  ScholarshipViewSet,
)

router = routers.DefaultRouter()
router.register(r"fee_setup", FeeSetupViewSet, basename="fee_setup")
router.register(r"scholarship", ScholarshipViewSet, basename="scholarship")


urlpatterns = [
    path("", include(router.urls)),
    path("fee-config/", FeeConfigView.as_view(), name="fee-config"),
    path(
        "activate-deactivate-fee-config/<pk>",
        ActivateDeactivateFeeConfig.as_view(),
        name="activate-deactivate-fee-config",
    ),
    path(
        "student-fee-collection/",
        StudentFeeCollectionView.as_view(),
        name="student-fee-collection",
    ),
 ]
