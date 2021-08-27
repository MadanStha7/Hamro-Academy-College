from rest_framework import viewsets, status
from staff.models import StaffAcademicInfo, Staff
from staff.administrator.serializers.staff_academicinfo import (
    StaffAcademicInfoSerializer,
)
from rest_framework.serializers import ValidationError
from rest_framework.generics import get_object_or_404

from common.administrator.viewset import CommonInfoViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


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

    @action(detail=False, methods=["get"], url_path="details")
    def staff_acdemic_info(self, request, *args, **kwargs):
        staff = self.request.query_params.get("staff", None)
        if staff:
            staff_obj = get_object_or_404(
                Staff, id=staff, institution=self.request.institution
            ).id
            staff_academic_info = StaffAcademicInfo.objects.filter(
                staff__id=staff_obj, institution=self.request.institution
            )
            if staff_academic_info:
                serializer = StaffAcademicInfoSerializer(staff_academic_info, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise ValidationError({"error": ["Staff id is required"]})
