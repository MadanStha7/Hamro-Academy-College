from django.db.models import F
from rest_framework import viewsets
from academics.models import Shift
from academics.administrator.serializers.shift import ShiftSerializer
from common.administrator.viewset import CommonInfoViewSet


class ShiftViewSet(CommonInfoViewSet):
    serializer_class = ShiftSerializer
    queryset = Shift.objects.none()

    def get_queryset(self):
        queryset = Shift.objects.filter(institution=self.request.institution)
        queryset = queryset.annotate(faculty_name=F("faculty__name"))
        return queryset
