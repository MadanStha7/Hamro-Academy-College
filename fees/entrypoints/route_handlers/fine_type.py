from rest_framework import filters

from common.administrator.viewset import CommonInfoViewSet
from fees.service_layer.serializers.fine_type import FineTypeSerializer
from fees.orm.models import FineType


class FineTypeViewSet(CommonInfoViewSet):
    """
    ViewSet for fine type in student fees
    """

    queryset = FineType.objects.none()
    serializer_class = FineTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        queryset = FineType.objects.filter(institution=self.request.institution)
        return queryset
