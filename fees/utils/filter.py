import django_filters

from fees.orm import models as orm


class FeeFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(field_name="grade__id", lookup_expr="contains")
    faculty = django_filters.UUIDFilter(
        field_name="faculty__id", lookup_expr="contains"
    )

    class Meta:
        model = orm.FeeSetup
        fields = ["grade", "faculty"]


class FeeConfigFilter(django_filters.rest_framework.FilterSet):
    grade = django_filters.UUIDFilter(
        field_name="subject_group__grade__id", lookup_expr="exact"
    )
    faculty = django_filters.UUIDFilter(
        field_name="subject_group__faculty__id", lookup_expr="exact"
    )

    class Meta:
        model = orm.FeeConfig
        fields = ["grade", "faculty"]
