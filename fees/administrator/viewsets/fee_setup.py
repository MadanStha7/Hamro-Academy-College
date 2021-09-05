from rest_framework import filters
from django.db.models import F
from common.administrator.viewset import CommonInfoViewSet
from fees.administrator.serializers.fee_setup import FeeSetupSerializer
from fees.models import FeeSetup
from fees.administrator.custom.filter import FeeFilter
from django_filters.rest_framework import DjangoFilterBackend


from common.utils import active_academic_session


class FeeSetupViewSet(CommonInfoViewSet):

    """
    ViewSet for student fees
    """

    queryset = FeeSetup.objects.none()
    serializer_class = FeeSetupSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_class = FeeFilter
    search_fields = ["name"]

    def get_queryset(self):
        queryset = FeeSetup.objects.filter(institution=self.request.institution)
        return queryset
