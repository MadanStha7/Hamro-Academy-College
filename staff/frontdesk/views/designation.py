from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from staff.frontdesk.serializers.designation import DesignationSerializer
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework.serializers import ValidationError
from staff.models import Designation


class DesignationListAPIView(ListAPIView):
    """Api to display a designation list in front desk officer"""

    serializer_class = DesignationSerializer
    queryset = Designation.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_queryset(self):
        queryset = Designation.objects.filter(institution=self.request.institution)
        return queryset


class DesignationRetrieveAPIView(RetrieveAPIView):
    """Api to display a  shift detail in front desk officer"""

    serializer_class = DesignationSerializer
    queryset = Designation.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_object(self):
        try:
            designation_obj = Designation.objects.get(
                id=self.kwargs.get("pk"), institution=self.request.institution
            )
            return designation_obj
        except Designation.DoesNotExist:
            raise ValidationError({"error": ["Designation object doesn't exist!"]})
