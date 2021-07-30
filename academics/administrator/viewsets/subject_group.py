from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from academics.administrator.serializers.subject_group import SubjectGroupSerializer
from academics.models import SubjectGroup
from common.administrator.viewset import CommonInfoViewSet


class SubjectGroupViewSet(CommonInfoViewSet):
    """
    Subject group list for the particular class.

    Like list of all the subjects of the particular class.
    """

    queryset = SubjectGroup.objects.none()
    serializer_class = SubjectGroupSerializer

    def get_queryset(self):
        grade = self.request.query_params.get("grade")
        section = self.request.query_params.get("section")
        faculty = self.request.query_params.get("faculty")
        subject = self.request.query_params.get("subject")
        queryset = SubjectGroup.objects.filter(institution=self.request.institution)
        if grade:
            queryset = queryset.filter(grade__id=grade)
        if faculty:
            queryset = queryset.filter(faculty__id=faculty)
        if subject:
            queryset = queryset.filter(subject__id=subject)
        if section:
            queryset = queryset.filter(faculty__id=faculty)
        return queryset
