from django.db.models import F
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from student.student.utils.student_active_academic import student_active_academic_info
from permissions.student import StudentPermission
from student.student.serializers.subject import StudentSubjectSerializer
from timetable.models import TimeTable


class StudentSubjectView(ListAPIView):
    """
    student viewset, where student can view all his subjects
    """

    permission_classes = (IsAuthenticated, StudentPermission)
    serializer_class = StudentSubjectSerializer
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        student_academic_id = student_active_academic_info(self.request.user)
        queryset = (
            TimeTable.objects.filter(
                grade=student_academic_id.grade,
                faculty=student_academic_id.faculty,
            )
            .order_by("subject")
            .distinct("subject")
        )
        queryset = queryset.annotate(
            subject_name=F("subject__name"),
            subject_credit_hour=F("subject__credit_hour"),
            subject_type=F("subject__subject_type"),
        )
        return queryset
