from rest_framework import filters

from common.administrator.viewset import CommonInfoViewSet
from fees.administrator.serializers.fine_type import FineTypeSerializer
from fees.models import  FineType


class FineTypeViewSet(CommonInfoViewSet):
    """
    ViewSet for fine type in student fees
    """

    queryset = FineType.objects.all()
    serializer_class = FineTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
