from rest_framework import viewsets
from staff.models import Document, Staff
from staff.administrator.serializers.document import DocumentSerializer
from common.administrator.viewset import CommonInfoViewSet
from rest_framework.response import Response
from rest_framework import status


class DocumentViewSet(CommonInfoViewSet):
    """
    CRUD for document of the staff.
    """

    serializer_class = DocumentSerializer
    queryset = Document.objects.none()

    def get_queryset(self):
        queryset = Document.objects.filter(institution=self.request.institution)
        return queryset

    def perform_create(self, serializer):
        staff = self.request.query_params.get("staff")
        if self.request.institution:
            serializer.save(
                staff=Staff(id=staff),
                created_by=self.request.user,
                institution=self.request.institution,
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
