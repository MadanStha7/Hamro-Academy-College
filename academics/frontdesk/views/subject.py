from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from academics.frontdesk.serializers.subject import SubjectSerializer
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework.serializers import ValidationError
from academics.models import Subject


class SubjectListAPIView(ListAPIView):
    """Api to display a Subject list in front desk officer"""

    serializer_class = SubjectSerializer
    queryset = Subject.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_queryset(self):
        queryset = Subject.objects.filter(institution=self.request.institution)
        return queryset


class SubjectRetrieveAPIView(RetrieveAPIView):
    """Api to display a  detail Subject list in front desk officer"""

    serializer_class = SubjectSerializer
    queryset = Subject.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_object(self):
        try:
            subject = Subject.objects.get(
                id=self.kwargs.get("pk"), institution=self.request.institution
            )
            return subject
        except Subject.DoesNotExist:
            raise ValidationError({"error": ["Subject object doesn't exist!"]})
