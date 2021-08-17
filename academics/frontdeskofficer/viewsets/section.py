from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from academics.frontdeskofficer.serializers.section import SectionSerializer
from permissions.front_desk_officer import FrontDeskOfficerPermission
from rest_framework.serializers import ValidationError
from academics.models import Section


class SectionListAPIView(ListAPIView):
    """Api to display a Section list in front desk officer"""

    serializer_class = SectionSerializer
    queryset = Section.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_queryset(self):
        queryset = Section.objects.filter(institution=self.request.institution)
        return queryset


class SectionRetrieveAPIView(RetrieveAPIView):
    """Api to display a  detail Section list in front desk officer"""

    serializer_class = SectionSerializer
    queryset = Section.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_object(self):
        try:
            section = Section.objects.get(
                id=self.kwargs.get("pk"), institution=self.request.institution
            )
            return section
        except Section.DoesNotExist:
            raise ValidationError({"error": ["Section object doesn't exist!"]})
