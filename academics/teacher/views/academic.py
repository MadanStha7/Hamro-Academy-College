from django.db.models import F
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from academics.teacher.serializers.academic import GradeSerializer, FacultySerializer, ShiftSerializer, \
    SectionSerializer
from permissions.teacher import TeacherPermission
from timetable.models import TimeTable


class GradeAPIView(ListAPIView):
    """
    api view of teacher for viewing the grade where he has been assigned
    """

    serializer_class = GradeSerializer
    permission_classes = (IsAuthenticated, TeacherPermission)
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        queryset = TimeTable.objects.filter(teacher=self.request.user,
                                            institution=self.request.institution).order_by(
            "start_time"
        ).order_by("grade").distinct("grade").annotate(grade_name=F("grade__name"),
                                                       section_name=F("section__name"),)
        return queryset


class FacultyAPIView(ListAPIView):
    """
    api view of teacher for viewing the faculty where he has been assigned
    """

    serializer_class = FacultySerializer
    permission_classes = (IsAuthenticated, TeacherPermission)
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        queryset = TimeTable.objects.filter(teacher=self.request.user,
                                            institution=self.request.institution
                                            ).order_by("faculty").distinct("faculty").annotate(
            faculty_name=F("faculty__name"))
        return queryset


class ShiftAPIView(ListAPIView):
    """
    api view of teacher for viewing the faculty where he has been assigned
    """

    serializer_class = ShiftSerializer
    permission_classes = (IsAuthenticated, TeacherPermission)
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        queryset = TimeTable.objects.filter(teacher=self.request.user,
                                            institution=self.request.institution).annotate(
            shift_name=F("shift__name"),
            section_name=F("section__name"),
            grade_name=F("grade__name"),
            subject_name=F("subject__name"),
            shift_time=F("start_time")
        )
        return queryset


class SectionAPIView(ListAPIView):
    """
    api view of teacher for viewing the section where he has been assigned
    """

    serializer_class = SectionSerializer
    permission_classes = (IsAuthenticated, TeacherPermission)
    queryset = TimeTable.objects.none()

    def get_queryset(self):
        queryset = TimeTable.objects.filter(teacher=self.request.user,
                                            institution=self.request.institution).order_by(
            "start_time"
        ).order_by("section").distinct("section").annotate(section_name=F("section__name"))
        return queryset







