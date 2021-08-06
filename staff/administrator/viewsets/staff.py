from rest_framework import viewsets
from staff.models import Staff
from staff.administrator.serializers.staff import StaffSerializer, StaffListSerializer
from common.administrator.viewset import CommonInfoViewSet
from django.db.models import F
from rest_framework.response import Response
from django.db.models import Count


class StaffViewSet(CommonInfoViewSet):
    """
    CRUD of the staff of college
    """

    serializer_class = StaffSerializer
    queryset = Staff.objects.none()

    def get_queryset(self):
        queryset = Staff.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(designation__name=F("designation__name"),)
        return queryset

    def list(self, request):
        """api to get list of serialzer of staff"""
        queryset = Staff.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(designation__name=F("designation__name"),contact_number=F("user__phone"),email=F("user__email"))
        serializer = StaffListSerializer(queryset, many=True)
        return Response(serializer.data)
