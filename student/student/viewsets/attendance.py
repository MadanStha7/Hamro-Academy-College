from django.db.models import F

from onlineclass.models import StudentOnlineClassAttendance
from onlineclass.administrator.serializers.online_class_attendance import (
    StudentOnlineClassAttendanceSerializer,
)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from permissions.student import StudentPermission
from student.student.utils.student_active_academic import student_active_academic_info


class StudentOnlineAttendanceView(ListAPIView):
    serializer_class = StudentOnlineClassAttendanceSerializer
    queryset = StudentOnlineClassAttendance.objects.none()
    permission_classes = (IsAuthenticated, StudentPermission)

    def get_queryset(self):
        student_academic_id = student_active_academic_info(self.request.user)
        print(student_academic_id)

        queryset = StudentOnlineClassAttendance.objects.filter(
            institution=self.request.institution, student_academic=student_academic_id
        )
        queryset = queryset.annotate(
            onlineclass_title=F("online_class__title"),
            student_name=F("student_academic__student__user__first_name"),
        )
        return queryset
