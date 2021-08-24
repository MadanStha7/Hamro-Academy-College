from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from academics.frontdesk.serializers.shift import ShiftSerializer
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework.serializers import ValidationError
from academics.models import Shift


class ShiftListAPIView(ListAPIView):
    """Api to display a Shift list in front desk officer"""

    serializer_class = ShiftSerializer
    queryset = Shift.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_queryset(self):
        queryset = Shift.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(faculty_name=F("faculty__name"))
        return queryset


class ShiftRetrieveAPIView(RetrieveAPIView):
    """Api to display a  shift detail in front desk officer"""

    serializer_class = ShiftSerializer
    queryset = Shift.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_queryset(self):
        queryset = Shift.objects.get(
            id=self.kwargs.get("pk"), institution=self.request.institution
        )
        queryset = queryset.annotate(faculty_name=F("faculty__name"))
        return queryset

    def get_object(self):
        try:
            shift = Shift.objects.annotate(faculty_name=F("faculty__name")).get(
                id=self.kwargs.get("pk"), institution=self.request.institution
            )
            return shift
        except Shift.DoesNotExist:
            raise ValidationError({"error": ["Shift object doesn't exist!"]})
