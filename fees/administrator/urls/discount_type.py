from django.urls import include, path
from rest_framework import routers

from fees.administrator.viewsets.discount_type import DiscountTypeViewSet

router = routers.DefaultRouter()
router.register(r"fee_discount", DiscountTypeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
