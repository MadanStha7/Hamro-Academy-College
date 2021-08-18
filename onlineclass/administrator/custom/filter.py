import django_filters
from onlineclass.models import OnlineClassInfo, StudentOnlineClassAttendance


class OnlineClassFilter(django_filters.rest_framework.FilterSet):
    days = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = OnlineClassInfo
        fields = ["days"]
