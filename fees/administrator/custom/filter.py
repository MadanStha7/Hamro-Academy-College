import django_filters

from fees.models import FeeSetup


class FeeFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(field_name="grade__id", lookup_expr="contains")
    faculty = django_filters.UUIDFilter(
        field_name="faculty__id", lookup_expr="contains"
    )

    class Meta:
        model = FeeSetup
        fields = ["grade", "faculty"]
