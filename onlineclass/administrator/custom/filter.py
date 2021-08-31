import django_filters
from onlineclass.models import OnlineClassInfo, StudentOnlineClassAttendance


class OnlineClassFilter(django_filters.rest_framework.FilterSet):
    days = django_filters.CharFilter(lookup_expr="icontains")
    grade = django_filters.UUIDFilter(field_name="grade__id", lookup_expr="exact")
    section = django_filters.UUIDFilter(field_name="section__id", lookup_expr="exact")
    faculty = django_filters.UUIDFilter(field_name="faculty__id", lookup_expr="exact")

    class Meta:
        model = OnlineClassInfo
        fields = ["days", "grade", "section", "faculty"]


class OnlineClassAttendanceFilter(django_filters.rest_framework.FilterSet):
    days = django_filters.CharFilter(lookup_expr="icontains")
    grade = django_filters.UUIDFilter(
        field_name="online_class__grade__id", lookup_expr="exact"
    )
    section = django_filters.UUIDFilter(
        field_name="online_class__section__id", lookup_expr="exact"
    )
    faculty = django_filters.UUIDFilter(
        field_name="online_class__faculty__id", lookup_expr="exact"
    )
    online_class = django_filters.UUIDFilter(
        field_name="online_class__id", lookup_expr="exact"
    )
    subject = django_filters.UUIDFilter(
        field_name="online_class__subject__id", lookup_expr="exact"
    )

    class Meta:
        model = StudentOnlineClassAttendance
        fields = ["days", "grade", "section", "faculty", "online_class", "subject"]
