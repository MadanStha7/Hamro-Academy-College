from django.db.models import F
from rest_framework import viewsets
from academics.models import Class
from academics.administrator.serializers.class_serializer import ClassSerializer
from common.administrator.viewset import CommonInfoViewSet


class ClassViewSet(CommonInfoViewSet):
    """
    view, where admin can view class
    """

    serializer_class = ClassSerializer
    queryset = Class.objects.none()

    def get_queryset(self):
        queryset = Class.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            faculty_name=F("faculty__name"), grade_name=F("grade__name")
        )
        return queryset
