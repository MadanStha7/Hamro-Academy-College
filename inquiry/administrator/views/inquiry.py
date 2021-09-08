from inquiry.models import Inquiry
from inquiry.administrator.serializers.inquiry import InquiryListSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from permissions.administrator import AdministratorPermission
from django.db.models import F
from project.custom.pagination import CustomPageSizePagination


class InquiryView(viewsets.ViewSet):
    """
    Views for listing or retrieving inqury for administrator.
    """

    serializer_class = InquiryListSerializer
    queryset = Inquiry.objects.none()
    permission_classes = (IsAuthenticated, AdministratorPermission)
    pagination_class = CustomPageSizePagination

    def list(self, request):
        """
        Api to get list of inquiry details
        """
        # institution = self.request.institution
        # queryset = self.get_queryset()
        # queryset = self.filter_queryset(queryset)
        # page = self.paginate_queryset(queryset)
        # page_ids = [i.id for i in page]
        # result = queryset.filter(id__in=page_ids)
        # result = result.annotate(
        #     faculty_name=F("faculty__name")),
        # result.annotate(faculty_name=F("faculty__name"))

        queryset = Inquiry.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(faculty_name=F("faculty__name"))
        paginator = CustomPageSizePagination()
        result_page = paginator.paginate_queryset(queryset, self.request)
        serializer = InquiryListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Inquiry.objects.annotate(faculty_name=F("faculty__name")).get(
            pk=pk, institution=self.request.institution
        )
        serializer = InquiryListSerializer(queryset)
        return Response(serializer.data)
