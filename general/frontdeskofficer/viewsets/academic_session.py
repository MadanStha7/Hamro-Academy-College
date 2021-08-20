from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from general.frontdeskofficer.serializers.academic_session import (
    AcademicSessionSerializer,
)
from permissions.front_desk_officer import FrontDeskOfficerPermission
from rest_framework.serializers import ValidationError
from general.models import AcademicSession


class AcademicSessionListAPIView(ListAPIView):
    """Api to display a AcademicSession list in front desk officer"""

    serializer_class = AcademicSessionSerializer
    queryset = AcademicSession.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_queryset(self):
        queryset = AcademicSession.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            grade_name=F("grade__name"),
        )
        return queryset


class AcademicSessionRetrieveAPIView(RetrieveAPIView):
    """Api to display a  detail AcademicSession list in front desk officer"""

    serializer_class = AcademicSessionSerializer
    queryset = AcademicSession.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_object(self):
        try:
            academic_session = AcademicSession.objects.annotate(
                grade_name=F("grade__name"),
            ).get(id=self.kwargs.get("pk"), institution=self.request.institution)
            # academic_session.annotate(grade_name=F("grade__name")
            return academic_session

        except AcademicSession.DoesNotExist:
            raise ValidationError({"error": ["AcademicSession object doesn't exist!"]})
