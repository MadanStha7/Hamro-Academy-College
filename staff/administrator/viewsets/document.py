from rest_framework import viewsets
from staff.models import Document
from staff.administrator.serializers.document import DocumentSerializer
from common.administrator.viewset import CommonInfoViewSet
from rest_framework.response import Response


class DocumentViewSet(CommonInfoViewSet):
    """
    CRUD for document of the staff.
    """

    serializer_class = DocumentSerializer
    queryset = Document.objects.none()

    def get_queryset(self):
        queryset = Document.objects.filter(institution=self.request.institution)
        return queryset
