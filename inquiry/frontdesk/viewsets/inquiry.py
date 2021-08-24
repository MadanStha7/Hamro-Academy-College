from inquiry.models import Inquiry
from inquiry.frontdesk.serializers.inquiry import InquirySerializer
from common.administrator.viewset import CommonInfoViewSet
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from rest_framework import filters


class InquiryViewSet(CommonInfoViewSet):
    """API for Inquiry model"""

    serializer_class = InquirySerializer
    queryset = Inquiry.objects.none()
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "contact_number",
    ]
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_queryset(self):
        queryset = Inquiry.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(faculty_name=F("faculty__name"))
        return queryset
