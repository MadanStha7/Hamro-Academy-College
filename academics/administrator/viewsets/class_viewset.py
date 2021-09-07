from django.db.models import F
from rest_framework.permissions import IsAuthenticated
from academics.administrator.custom_filter import ClassFilter
from academics.models import Class
from academics.administrator.serializers.class_serializer import ClassSerializer
from django_filters import rest_framework as filters
from common.administrator.viewset import CommonInfoViewSet
from permissions.administrator import AdministratorPermission


class ClassViewSet(CommonInfoViewSet):
    """
    view, where admin can view class
    """

    serializer_class = ClassSerializer
    queryset = Class.objects.none()
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, AdministratorPermission)
    filter_class = ClassFilter

    def get_queryset(self):
        queryset = Class.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(
            faculty_name=F("faculty__name"), grade_name=F("grade__name")
        )
        return queryset
