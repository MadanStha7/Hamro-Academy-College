import django_filters
from general.models import AcademicSession


class AcademicSessionFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(field_name="grade__id", lookup_expr="exact")
    faculty = django_filters.UUIDFilter(field_name="faculty__id", lookup_expr="exact")

    class Meta:
        model = AcademicSession
        fields = ["grade", "faculty"]
