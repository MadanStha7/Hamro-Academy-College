import django_filters
from onlineclass.models import StudentOnlineClassAttendance


class AttendanceFilter(django_filters.rest_framework.FilterSet):
    subject = django_filters.UUIDFilter(
        field_name="online_class__subject__id", lookup_expr="exact"
    )

    class Meta:
        model = StudentOnlineClassAttendance
        fields = ["subject"]
