from rest_framework import filters
from common.administrator.viewset import CommonInfoViewSet
from fees.administrator.serializers.discount_type import DiscountTypeSerializer
from fees.models import DiscountType


class DiscountTypeViewSet(CommonInfoViewSet):
    """
    Viewset for discount type in student fees
    """

    queryset = DiscountType.objects.all()
    serializer_class = DiscountTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
