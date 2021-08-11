from academics.administrator.custom_filter import SubjectGroupFilter
from academics.administrator.serializers.subject_group import SubjectGroupSerializer
from academics.models import SubjectGroup
from common.administrator.viewset import CommonInfoViewSet
from django_filters import rest_framework as filters


class SubjectGroupViewSet(CommonInfoViewSet):
    """
    Subject group list for the particular class.
    """

    queryset = SubjectGroup.objects.none()
    serializer_class = SubjectGroupSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SubjectGroupFilter

    def get_queryset(self):
        queryset = SubjectGroup.objects.filter(institution=self.request.institution)

        return queryset
