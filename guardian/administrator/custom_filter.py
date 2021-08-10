import django_filters

from guardian.models import StudentGuardianInfo


class StudentGuardianFilter(django_filters.rest_framework.FilterSet):
    student = django_filters.UUIDFilter(field_name='student_info__id', lookup_expr='exact')

    class Meta:
        model = StudentGuardianInfo
        fields = ["student"]


