from rest_framework import viewsets
from staff.models import Staff
from staff.administrator.serializers.staff import StaffSerializer
from common.administrator.viewset import CommonInfoViewSet
from django.db.models import F


class StaffViewSet(CommonInfoViewSet):
    """
    CRUD of the staff of college
    """

    serializer_class = StaffSerializer
    queryset = Staff.objects.none()

    def get_queryset(self):
        queryset = Staff.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(designation__name=F("designation__name"))
        return queryset
