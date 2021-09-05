from staff.models import Staff, StaffAcademicInfo
from django_filters import rest_framework
from django.db.models import Q


class StaffFilter(rest_framework.FilterSet):

    designation = rest_framework.UUIDFilter(lookup_expr="exact")
    department = rest_framework.UUIDFilter(
        field_name="staff_academic_info__department", lookup_expr="exact"
    )

    class Meta:
        model = Staff
        fields = ["designation", "department"]
