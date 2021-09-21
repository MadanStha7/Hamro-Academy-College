from django.urls import include, path
from rest_framework import routers
from fees.entrypoints.route_handlers.administrator import (
    FeeSetupViewSet,
    FeeConfigView,
    ActivateDeactivateFeeConfig,
    StudentFeeCollectionView,
    StudentCollectedFeeInvoiceViewset,
    UpdateStudentPaidFeeConfigView,
    StudentFeeInvoiceView,
)
from fees.entrypoints.route_handlers.discount_type import DiscountTypeViewSet
from fees.entrypoints.route_handlers.fine_type import FineTypeViewSet

router = routers.DefaultRouter()
router.register(r"fee_setup", FeeSetupViewSet, basename="fee_setup")
router.register("discount_type", DiscountTypeViewSet)
router.register("fine_type", FineTypeViewSet)
router.register(
    "student-fee-collected",
    StudentCollectedFeeInvoiceViewset,
    basename="fee-collection",
)


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
    path(
        "update_paid_fee_config/",
        UpdateStudentPaidFeeConfigView.as_view(),
        name="update-paid-fee-config",
    ),
    path("fee-invoice/", StudentFeeInvoiceView.as_view(), name="student-fee-invoice"),
]
