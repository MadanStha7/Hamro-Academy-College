from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from academics.frontdesk.serializers.class_url import (
    ClassSerializer,
    OnlineclassFilterSerializer,
)
from django_filters import rest_framework as filters
from academics.administrator.custom_filter import ClassFilter
from permissions.front_desk_officer import FrontDeskPermission
from rest_framework.serializers import ValidationError
from academics.models import Class
from rest_framework.response import Response


class ClassListAPIView(ListAPIView):
    """Api to display a Class list in front desk officer"""

    serializer_class = ClassSerializer
    queryset = Class.objects.none()
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, FrontDeskPermission)
    filter_class = ClassFilter

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
            faculty_name=F("faculty__name"), grade_name=F("grade__name")
        )
        serializer = ClassSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class ClassRetrieveAPIView(RetrieveAPIView):
    """Api to display a  detail Class list in front desk officer"""

    serializer_class = ClassSerializer
    queryset = Class.objects.none()
    permission_classes = (IsAuthenticated, FrontDeskPermission)

    def get_object(self):
        try:
            class_obj = Class.objects.annotate(
                faculty_name=F("faculty__name"), grade_name=F("grade__name")
            ).get(id=self.kwargs.get("pk"), institution=self.request.institution)
            return class_obj
        except Class.DoesNotExist:
            raise ValidationError({"error": ["Class object doesn't exist!"]})
