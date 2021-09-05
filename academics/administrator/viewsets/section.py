from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from academics.administrator.serializers.class_serializer import SectionListSerializer
from academics.models import Section, Class
from academics.administrator.serializers.section import SectionSerializer
from common.administrator.viewset import CommonInfoViewSet
from rest_framework import filters

from student.administator.custom_fiter import SectionFilter


class SectionViewSet(CommonInfoViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.none()

    def get_queryset(self):
        queryset = Section.objects.filter(institution=self.request.institution)
        return queryset


class SectionListView(ListAPIView):
    queryset = Class.objects.none()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_class = SectionFilter

    def get_queryset(self):
        queryset = Class.objects.filter(institution=self.request.institution)
        return queryset

    def list(self, request, *args, **kwargs):
        """api to get list of grade"""
        institution = self.request.institution
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        page_ids = [i.id for i in page]
        result = queryset.filter(id__in=page_ids)
        result = result.annotate(
            grade_name=F("grade__name")
        )
        serializer = SectionListSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)



