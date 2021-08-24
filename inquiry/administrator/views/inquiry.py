from inquiry.models import Inquiry
from inquiry.administrator.serializers.inquiry import InquiryListSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from permissions.administrator import AdministratorPermission
from django.db.models import F


class InquiryView(viewsets.ViewSet):
    """
    Views for listing or retrieving inqury for administrator.
    """

    serializer_class = InquiryListSerializer
    queryset = Inquiry.objects.none()
    permission_classes = (IsAuthenticated, AdministratorPermission)

    def list(self, request):
        queryset = Inquiry.objects.filter(
            institution=self.request.institution
        ).annotate(faculty_name=F("faculty__name"))
        serializer = InquiryListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Inquiry.objects.annotate(faculty_name=F("faculty__name")).get(
            pk=pk, institution=self.request.institution
        )
        serializer = InquiryListSerializer(queryset)
        return Response(serializer.data)
