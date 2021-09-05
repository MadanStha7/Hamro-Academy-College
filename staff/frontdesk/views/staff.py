from staff.administrator.custom.filters import StaffFilter
from staff.models import Staff
from django.db.models import F
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from staff.frontdesk.serializers.staff import StaffListSerializer
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework.serializers import ValidationError


class StaffListAPIView(ListAPIView):
    """Api to display a staff list in front desk officer"""

    serializer_class = StaffListSerializer
    queryset = Staff.objects.none()
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__phone",
    ]
    filter_class = StaffFilter
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_queryset(self):
        queryset = Staff.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            designation_name=F("designation__name"),
            staff_contact_number=F("user__phone"),
            staff_email=F("user__email"),
            staff_first_name=F("user__first_name"),
            staff_last_name=F("user__last_name"),
            staff_faculty=F("staff_academic_info__faculty__name"),
        )
        return queryset


class StaffRetrieveAPIView(RetrieveAPIView):
    """Api to display a  shift detail in front desk officer"""

    serializer_class = StaffListSerializer
    queryset = Staff.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_object(self):
        try:
            Staff_obj = Staff.objects.annotate(
                designation_name=F("designation__name"),
                staff_contact_number=F("user__phone"),
                staff_email=F("user__email"),
                staff_first_name=F("user__first_name"),
                staff_last_name=F("user__last_name"),
                staff_faculty=F("staff_academic_info__faculty__name"),
            ).get(id=self.kwargs.get("pk"), institution=self.request.institution)
            return Staff_obj
        except Staff.DoesNotExist:
            raise ValidationError({"error": ["Staff object doesn't exist!"]})
