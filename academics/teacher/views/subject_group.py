from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from academics.administrator.custom_filter import SubjectGroupFilter
from academics.administrator.serializers.subject_group import SubjectGroupSerializer
from academics.models import SubjectGroup
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class SubjectGroupView(ListAPIView):
    """
    CRUD for Subject Group .
    """
    queryset = SubjectGroup.objects.none()
    serializer_class = SubjectGroupSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_class = SubjectGroupFilter
    search_fields = ["grade__name", "faculty__name", "section__name"]

    def get_queryset(self):
        grade = self.request.query_params.get("grade")
        if grade:
            queryset = SubjectGroup.objects.filter(grade=grade,
                                                   institution=self.request.institution)
            return queryset
        else:
            raise ValidationError({"grade": ["This field is required query param"]})
