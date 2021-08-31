from django.db.models import F
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from student.student.utils.student_active_academic import student_active_academic_info
from permissions.student import StudentPermission
from timetable.student.serializers.grade_timetable import (
    StudentGradeTimetableSerializer,
)
from timetable.models import TimeTable


class StudentGradeTimetableView(ListAPIView):
    """
    student viewset, where student can view all timetable of his grade
    """

    permission_classes = (IsAuthenticated, StudentPermission)
    serializer_class = StudentGradeTimetableSerializer
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        student_academic_id = student_active_academic_info(self.request.user)
        queryset = TimeTable.objects.filter(
            grade=student_academic_id.grade,
            faculty=student_academic_id.faculty,
        )
        queryset = queryset.annotate(
            grade_name=F("grade__name"),
            section_name=F("section__name"),
            subject_name=F("subject__name"),
            subject_credit_hour=F("subject__credit_hour"),
            subject_type=F("subject__subject_type"),
            faculty_name=F("faculty__name"),
        )
        return queryset
