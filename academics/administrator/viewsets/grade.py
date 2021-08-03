from rest_framework import viewsets
from academics.models import Grade
from academics.administrator.serializers.grade import GradeSerializer
from common.administrator.viewset import CommonInfoViewSet


class GradeViewSet(CommonInfoViewSet):
    serializer_class = GradeSerializer
    queryset = Grade.objects.none()

    def get_queryset(self):
        queryset = Grade.objects.filter(institution=self.request.institution)
        return queryset
