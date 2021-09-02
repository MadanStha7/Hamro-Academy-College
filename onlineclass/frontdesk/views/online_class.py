from onlineclass.frontdesk.serializers.online_class import OnlineClassSerializer
from onlineclass.models import OnlineClassInfo
from onlineclass.administrator.custom.filter import OnlineClassFilter
from rest_framework.permissions import IsAuthenticated
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from collections import defaultdict
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from project.custom.pagination import CustomPageSizePagination


class OnlineClassListAPIView(ListAPIView):
    """Api to display a Online class list in front desk officer"""

    serializer_class = OnlineClassSerializer
    queryset = OnlineClassInfo.objects.none()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OnlineClassFilter
    permission_classes = (IsAuthenticated, FrontDeskPermission)
    pagination_class = CustomPageSizePagination

    def list(self, request):
        """api to get list of online class in front desk filtering days"""

        queryset = OnlineClassInfo.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            faculty_name=F("faculty__name"),
            grade_name=F("grade__name"),
            section_name=F("section__name"),
            subject_name=F("subject__name"),
        )
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OnlineClassSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
