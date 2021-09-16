import django_filters
from onlineclass.models import StudentOnlineClassAttendance


class AttendanceFilter(django_filters.rest_framework.FilterSet):
    subject = django_filters.UUIDFilter(
        field_name="online_class__subject__id", lookup_expr="exact"
    )
    from_date = django_filters.DateFilter(field_name="created_on", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="created_on", lookup_expr="lte")

    class Meta:
        model = StudentOnlineClassAttendance
        fields = ["subject", "from_date", "end_date"]
