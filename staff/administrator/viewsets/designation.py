from rest_framework import viewsets
from staff.models import Designation
from staff.administrator.serializers.designation import DesignationSerializer
from common.administrator.viewset import CommonInfoViewSet
from rest_framework.response import Response


class DesignationViewSet(CommonInfoViewSet):
    """
    CRUD for Designation of the staff.
    """

    serializer_class = DesignationSerializer
    queryset = Designation.objects.none()

    def get_queryset(self):
        queryset = Designation.objects.filter(institution=self.request.institution)
        return queryset
