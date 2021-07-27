from rest_framework import viewsets
from academics.models import Section
from academics.administrator.serializers.section import SectionSerializer
from common.administrator.viewset import CommonInfoViewSet


class SectionViewSet(CommonInfoViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.none()

    def get_queryset(self):
        queryset = Section.objects.filter(institution=self.request.institution)
        return queryset
