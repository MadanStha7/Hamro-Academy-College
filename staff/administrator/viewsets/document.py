from rest_framework import viewsets
from staff.models import Document, Staff
from staff.administrator.serializers.document import DocumentSerializer
from common.administrator.viewset import CommonInfoViewSet
from permissions.administrator_or_teacher_or_frontdesk import (
    AdministratorOrTeacherOrFrontDeskOPermission,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404


class StaffDocumentViewSet(CommonInfoViewSet):
    """
    CRUD for document of the staff.
    """

    serializer_class = DocumentSerializer
    queryset = Document.objects.none()

    def get_queryset(self):
        queryset = Document.objects.filter(institution=self.request.institution)
        print("queryset", queryset)
        return queryset

    def perform_create(self, serializer):
        staff = self.request.query_params.get("staff")
        if self.request.institution:
            serializer.save(
                staff=Staff.objects.get(id=staff),
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

    @action(
        permission_classes=(
            IsAuthenticated,
            AdministratorOrTeacherOrFrontDeskOPermission,
        ),
        detail=False,
        methods=["get"],
        url_path="details",
    )
    def staff_acdemic_info(self, request, *args, **kwargs):
        staff = self.request.query_params.get("staff", None)
        if staff:
            staff_obj = get_object_or_404(
                Staff, id=staff, institution=self.request.institution
            )
            document_data = Document.objects.filter(
                staff=staff_obj, institution=self.request.institution
            )
            if document_data:
                serializer = DocumentSerializer(document_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise ValidationError({"error": ["staff has no documents"]})
        else:
            raise ValidationError({"error": ["Staff id is required"]})
