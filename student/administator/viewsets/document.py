from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from common.administrator.viewset import CommonInfoViewSet
from student.administator.custom_fiter import StudentDocumentFilter
from student.administator.serializer.document import StudentDocumentSerializer

from student.models import StudentDocument, StudentInfo


class StudentDocumentViewSet(CommonInfoViewSet):
    """
    CRUD for document of student
    """

    queryset = StudentDocument.objects.none()
    serializer_class = StudentDocumentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = StudentDocumentFilter

    def get_queryset(self):
        queryset = StudentDocument.objects.filter(
            institution=self.request.institution
        )
        return queryset

    def perform_create(self, serializer):
        student = self.request.query_params.get("student")
        if student:
            if self.request.institution:
                serializer.save(
                    student=StudentInfo(id=student),
                    created_by=self.request.user,
                    institution=self.request.institution
                )
        else:
            raise ValidationError(
                {
                    "message": ["Student id is required in query param"]
                }
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        document = get_object_or_404(
            StudentDocument, id=self.kwargs.get("pk"), created_by=self.request.user
        )
        document.delete()
        return Response(
            {"message": f"object {self.kwargs.get('pk')} deleted successfully"}
        )