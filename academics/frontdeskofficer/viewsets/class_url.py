from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from academics.frontdeskofficer.serializers.class_url import ClassSerializer
from permissions.front_desk_officer import FrontDeskOfficerPermission
from rest_framework.serializers import ValidationError
from academics.models import Class


class ClassListAPIView(ListAPIView):
    """Api to display a Class list in front desk officer"""

    serializer_class = ClassSerializer
    queryset = Class.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_queryset(self):
        queryset = Class.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            faculty_name=F("faculty__name"), grade_name=F("grade__name")
        )
        return queryset


class ClassRetrieveAPIView(RetrieveAPIView):
    """Api to display a  detail Class list in front desk officer"""

    serializer_class = ClassSerializer
    queryset = Class.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskOfficerPermission)

    def get_object(self):
        try:
            class_obj = Class.objects.annotate(
                faculty_name=F("faculty__name"), grade_name=F("grade__name")
            ).get(id=self.kwargs.get("pk"), institution=self.request.institution)
            return class_obj
        except Class.DoesNotExist:
            raise ValidationError({"error": ["Class object doesn't exist!"]})
