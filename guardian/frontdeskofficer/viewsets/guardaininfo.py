from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from guardian.frontdeskofficer.serializer.guardianinfo import GuardianInfoSerializer
from permissions.front_desk_officer import FrontDeskOfficerPermission
from guardian.models import StudentGuardianInfo
from guardian.administrator.custom_filter import StudentGuardianFilter
from student.administator.custom_fiter import StudentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.serializers import ValidationError


class GuardianListAPIView(ListAPIView):
    """Api to display a guardian list in front desk officer"""

    queryset = StudentGuardianInfo.objects.none()
    serializer_class = GuardianInfoSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["user__first_name", "user__last_name", "user__phone"]
    filter_class = StudentGuardianFilter
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_queryset(self):
        queryset = StudentGuardianInfo.objects.filter(
            institution=self.request.institution
        )
        queryset = queryset.annotate(
            guardian_first_name=F("user__first_name"),
            guardian_last_name=F("user__last_name"),
            guardian_phone_number=F("user__phone"),
            guardian_email=F("user__email"),
        )
        queryset = self.filter_queryset(queryset)
        return queryset


class GuardianRetrieveAPIView(RetrieveAPIView):
    """Api to display a  shift detail in front desk officer"""

    serializer_class = GuardianInfoSerializer
    queryset = StudentGuardianInfo.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_object(self):
        try:
            guardian_info = StudentGuardianInfo.objects.annotate(
                guardian_first_name=F("user__first_name"),
                guardian_last_name=F("user__last_name"),
                guardian_phone_number=F("user__phone"),
                guardian_email=F("user__email"),
            ).get(id=self.kwargs.get("pk"), institution=self.request.institution)
            return guardian_info
        except StudentGuardianInfo.DoesNotExist:
            raise ValidationError({"error": ["GuardianInfo object doesn't exist!"]})
