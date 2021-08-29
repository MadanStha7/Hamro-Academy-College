from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView


from academics.administrator.serializers.class_serializer import ClassSerializer, GradeListSerializer
from academics.models import Grade, Class
from academics.administrator.serializers.grade import GradeSerializer
from common.administrator.viewset import CommonInfoViewSet
from student.administator.custom_fiter import GradeFilter


class GradeViewSet(CommonInfoViewSet):
    serializer_class = GradeSerializer
    queryset = Grade.objects.none()

    def get_queryset(self):
        queryset = Grade.objects.filter(institution=self.request.institution)
        return queryset


class GradeListView(ListAPIView):
    serializer_class = GradeListSerializer
    queryset = Class.objects.none()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_class = GradeFilter

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
        serializer = GradeListSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

