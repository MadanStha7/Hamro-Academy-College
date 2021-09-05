from django.db.models import F
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from academics.custom_validations import validate_teacher_grade
from academics.models import Grade

from academics.teacher.serializers.subject import TeacherSubjectSerializer
from permissions.teacher import TeacherPermission
from timetable.models import TimeTable


class TeacherSubjectView(ListAPIView):
    """
    teacher viewset, where teacher can view all the subject, teacher has been assigned to
    """

    permission_classes = (IsAuthenticated, TeacherPermission)
    serializer_class = TeacherSubjectSerializer
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        grade = self.request.query_params.get("grade")
        queryset = (
            TimeTable.objects.filter(
                teacher=self.request.user,
                institution=self.request.institution,
                academic_session__status=True,
            )
            .order_by("subject")
            .distinct("subject")
        ).annotate(
            section_name=F("section__name"),
            shift_name=F("shift__name"),
            grade_name=F("grade__name"),
            faculty_name=F("faculty__name"),
            teacher_first_name=F("teacher__first_name"),
            teacher_last_name=F("teacher__last_name"),
            subject_name=F("subject__name"),
            credit_hour=F("subject__credit_hour"),
            subject_type=F("subject__subject_type"),
            is_optional=F("subject__is_optional"),
        )
        if grade:
            validate_teacher_grade(Grade(id=grade), self.request.user)
            queryset = queryset.filter(grade__id=grade)
            queryset = queryset
        return queryset
