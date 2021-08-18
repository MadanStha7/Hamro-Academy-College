from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from academics.frontdeskofficer.serializers.apply_shift import ApplyShiftSerializer
from permissions.front_desk_officer import FrontDeskOfficerPermission
from rest_framework.serializers import ValidationError
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from academics.administrator.custom_filter import ApplyShiftFilter
from academics.models import ApplyShift


class ApplyShiftListAPIView(ListAPIView):
    """Api to display a apply shift list in front desk officer"""

    serializer_class = ApplyShiftSerializer
    queryset = ApplyShift.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [
        "shift__name",
        "grade__name",
        "section__name",
        "faculty__name",
    ]
    filter_class = ApplyShiftFilter

    def get_queryset(self):
        queryset = ApplyShift.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            shift_name=F("shift__name"),
            shift_start_time=F("shift__start_time"),
            shift_end_time=F("shift__end_time"),
            grade_name=F("grade__name"),
            faculty_name=F("faculty__name"),
            section_name=F("section__name"),
        )
        return queryset


class ApplyShiftRetrieveAPIView(RetrieveAPIView):
    """Api to display a  detail ApplyShift list in front desk officer"""

    serializer_class = ApplyShiftSerializer
    queryset = ApplyShift.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_object(self):
        try:
            applyshift_obj = ApplyShift.objects.annotate(
                shift_name=F("shift__name"),
                shift_start_time=F("shift__start_time"),
                shift_end_time=F("shift__end_time"),
                grade_name=F("grade__name"),
                faculty_name=F("faculty__name"),
                section_name=F("section__name"),
            ).get(id=self.kwargs.get("pk"), institution=self.request.institution)
            return applyshift_obj
        except ApplyShift.DoesNotExist:
            raise ValidationError({"error": ["ApplyShift object doesn't exist!"]})
