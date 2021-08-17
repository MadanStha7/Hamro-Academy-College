from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from academics.frontdeskofficer.serializers.faculty import FacultySerializer
from permissions.front_desk_officer import FrontDeskOfficerPermission
from rest_framework.serializers import ValidationError
from academics.models import Faculty


class FacultyListAPIView(ListAPIView):
    """Api to display a faculty list in front desk officer"""

    serializer_class = FacultySerializer
    queryset = Faculty.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_queryset(self):
        queryset = Faculty.objects.filter(institution=self.request.institution)
        return queryset


class FacultyRetrieveAPIView(RetrieveAPIView):
    """Api to display a  detail faculty list in front desk officer"""

    serializer_class = FacultySerializer
    queryset = Faculty.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_object(self):
        try:
            faculty = Faculty.objects.get(
                id=self.kwargs.get("pk"), institution=self.request.institution
            )
            return faculty
        except Faculty.DoesNotExist:
            raise ValidationError({"error": ["Faculty object doesn't exist!"]})
