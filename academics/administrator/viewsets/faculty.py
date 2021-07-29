from rest_framework import viewsets
from academics.models import Faculty
from academics.administrator.serializers.faculty import FacultySerializer
from common.administrator.viewset import CommonInfoViewSet
from rest_framework.response import Response
from rest_framework import status


class FacultyViewSet(CommonInfoViewSet):
    """API for faculty model"""

    serializer_class = FacultySerializer
    queryset = Faculty.objects.none()

    def get_queryset(self):
        queryset = Faculty.objects.filter(institution=self.request.institution)
        return queryset
