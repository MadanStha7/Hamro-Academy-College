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

    def perform_create(self, serializer):
        """
        Create the subject group name and store the data in the database.
        """
        subject = self.request.data.get("subject")
        section = self.request.data.get("section")
        if self.request.institution:
            serializer.save(
                subject=subject,
                section=section,
                created_by=self.request.user,
                institution=self.request.institution,
            )
        else:
            return Response(
                {
                    "error": {
                        "subject_group_name": [
                            "Subject group with this name already exists"
                        ]
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_update(self, serializer):
        """
        Update the subject group and store the data in the database.
        """
        subject = self.request.data.get("subject")
        if self.request.institution:
            serializer.save(
                subject=subject,
            )
        else:
            return Response(
                {
                    "error": {
                        "subject_subject_group_name": [
                            "Subject group with this name already exists"
                        ]
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
