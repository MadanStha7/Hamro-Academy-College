from django.db.models import F, Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from onlineclass.administrator.custom.filter import OnlineClassAttendanceFilter
from onlineclass.models import StudentOnlineClassAttendance
from onlineclass.administrator.serializers.online_class_attendance import (
    StudentOnlineClassAttendanceSerializer,
)
from common.administrator.viewset import CommonInfoViewSet


class StudentOnlineClassAttendanceViewSet(CommonInfoViewSet):
    serializer_class = StudentOnlineClassAttendanceSerializer
    queryset = StudentOnlineClassAttendance.objects.none()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OnlineClassAttendanceFilter

    def get_queryset(self):
        queryset = StudentOnlineClassAttendance.objects.filter(
            institution=self.request.institution
        )
        queryset = queryset.annotate(
            onlineclass_title=F("online_class__title"),
            student_full_name=Concat(
                F("student_academic__student__user__first_name"),
                Value(" "),
                F("student_academic__student__user__last_name"),
            ),
        )

        return queryset
