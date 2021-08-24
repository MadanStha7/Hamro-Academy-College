from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from academics.frontdesk.serializers.grade import GradeSerializer
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework.serializers import ValidationError
from academics.models import Grade


class GradeListAPIView(ListAPIView):
    """Api to display a Grade list in front desk officer"""

    serializer_class = GradeSerializer
    queryset = Grade.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_queryset(self):
        queryset = Grade.objects.filter(institution=self.request.institution)
        return queryset


class GradeRetrieveAPIView(RetrieveAPIView):
    """Api to display a  detail Grade list in front desk officer"""

    serializer_class = GradeSerializer
    queryset = Grade.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_object(self):
        try:
            grade = Grade.objects.get(
                id=self.kwargs.get("pk"), institution=self.request.institution
            )
            return grade
        except Grade.DoesNotExist:
            raise ValidationError({"error": ["Grade object doesn't exist!"]})
