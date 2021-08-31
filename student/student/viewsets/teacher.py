from django.db.models import F, Value
from django.db.models.functions import Concat
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from student.student.utils.student_active_academic import student_active_academic_info
from permissions.student import StudentPermission
from student.student.serializers.teacher import StudentTeacherSerializer
from timetable.models import TimeTable


class StudentTeacherView(ListAPIView):
    """
    student viewset, where student can view his teachers
    """

    permission_classes = (IsAuthenticated, StudentPermission)
    serializer_class = StudentTeacherSerializer

    def get_queryset(self):
        student_academic_id = student_active_academic_info(self.request.user)
        queryset = (
            TimeTable.objects.filter(
                grade=student_academic_id.grade,
                faculty=student_academic_id.faculty,
            )
                .order_by("teacher")
                .distinct("teacher")
        )
        queryset = queryset.annotate(
            teacher_full_name=Concat(
                F("teacher__first_name"),
                Value(" "),
                F("teacher__last_name"),
            ),
            subject_name=F("subject__name"),
        )
        return queryset
