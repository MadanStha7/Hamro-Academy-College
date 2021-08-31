from django.db.models import F
from onlineclass.models import StudentOnlineClassAttendance
from onlineclass.student.serializers.attendance import (
    StudentOnlineClassAttendanceSerializer,
)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from permissions.student import StudentPermission
from student.student.utils.student_active_academic import student_active_academic_info
from student.student.utils.attendance_filter import AttendanceFilter
from django_filters import rest_framework as filters


class StudentOnlineAttendanceView(ListAPIView):
    serializer_class = StudentOnlineClassAttendanceSerializer
    permission_classes = (IsAuthenticated, StudentPermission)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AttendanceFilter

    def get_queryset(self):
        student_academic_id = student_active_academic_info(self.request.user)

        queryset = StudentOnlineClassAttendance.objects.filter(
            institution=self.request.institution, student_academic=student_academic_id
        )
        queryset = queryset.annotate(
            onlineclass_title=F("online_class__title"),
            subject_name=F("online_class__subject__name"),
        )
        return queryset
