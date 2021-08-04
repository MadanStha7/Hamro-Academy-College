from rest_framework import viewsets
from staff.models import StaffAcademicInfo
from staff.administrator.serializers.staff_academicinfo import (
    StaffAcademicInfoSerializer,
)
from common.administrator.viewset import CommonInfoViewSet


class StaffAcademicInfoViewSet(CommonInfoViewSet):
    """
    CRUD of the staff academic info of college
    """

    serializer_class = StaffAcademicInfoSerializer
    queryset = StaffAcademicInfo.objects.none()

    def get_queryset(self):
        queryset = StaffAcademicInfo.objects.filter(
            institution=self.request.institution
        )
        # queryset = queryset.annotate(designation__name=F("designation__name"))
        return queryset
