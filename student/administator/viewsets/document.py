from rest_framework import status
from rest_framework.response import Response

from common.administrator.viewset import CommonInfoViewSet
from student.administator.serializer.document import StudentDocumentSerializer

from student.models import StudentDocument, StudentInfo


class StudentDocumentViewSet(CommonInfoViewSet):
    """
    CRUD for student category
    """

    queryset = StudentDocument.objects.none()
    serializer_class = StudentDocumentSerializer

    def get_queryset(self):
        queryset = StudentDocument.objects.filter(
            institution=self.request.institution
        )
        return queryset

    def perform_create(self, serializer):
        student = self.request.query_params.get("student")

        if self.request.institution:
            serializer.save(
                student=StudentInfo(id=student),
                created_by=self.request.user,
                institution=self.request.institution
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

