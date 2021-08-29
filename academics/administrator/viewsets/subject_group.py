from academics.administrator.custom_filter import SubjectGroupFilter
from academics.administrator.serializers.subject_group import SubjectGroupSerializer
from academics.models import SubjectGroup
from common.administrator.viewset import CommonInfoViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class SubjectGroupViewSet(CommonInfoViewSet):
    """
    CRUD for Subject Group .
    """
    queryset = SubjectGroup.objects.none()
    serializer_class = SubjectGroupSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_class = SubjectGroupFilter
    search_fields = ["grade__name", "faculty__name", "section__name"]

    def get_queryset(self):
        queryset = SubjectGroup.objects.filter(institution=self.request.institution)

        return queryset
