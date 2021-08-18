from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from academics.frontdeskofficer.serializers.subject_group import SubjectGroupSerializer
from permissions.front_desk_officer import FrontDeskOfficerPermission
from academics.administrator.custom_filter import SubjectGroupFilter
from rest_framework.serializers import ValidationError
from academics.models import SubjectGroup
from django_filters import rest_framework as filters
from django.db.models import F


class SubjectGroupListAPIView(ListAPIView):
    """Api to display a SubjectGroup list in front desk officer"""

    serializer_class = SubjectGroupSerializer
    queryset = SubjectGroup.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SubjectGroupFilter

    def get_queryset(self):
        queryset = SubjectGroup.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            grade_name=F("grade__name"),
            faculty_name=F("faculty__name"),
        )
        return queryset


class SubjectGroupRetrieveAPIView(RetrieveAPIView):
    """Api to display a  detail SubjectGroup list in front desk officer"""

    serializer_class = SubjectGroupSerializer
    queryset = SubjectGroup.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_object(self):
        try:
            return SubjectGroup.objects.annotate(
                grade_name=F("grade__name"),
                faculty_name=F("faculty__name"),
            ).get(id=self.kwargs.get("pk"), institution=self.request.institution)
        except SubjectGroup.DoesNotExist:
            raise ValidationError({"error": ["SubjectGroup object doesn't exist!"]})
